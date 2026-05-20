"""Roll D: Automation Script.

See fail ühendab Roll A, B ja C moodulid üheks pipeline'iks:
extract -> transform -> validate -> export. Käivitamiseks kasuta
`python week-08/team/pipeline.py`.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

sys.path.append(str(Path(__file__).resolve().parent.parent))

from data_fetcher import create_supabase_client, fetch_customers, fetch_products, fetch_sales, sample_data
from notifications import send_pipeline_notification
from transform import (
    build_business_interpretation,
    calculate_kpis,
    calculate_rfm,
    calculate_segment_summary,
    calculate_weekly_aggregates,
    clean_data,
    merge_datasets,
)
from visualize_export import export_results


ROOT = Path(__file__).resolve().parent
CONFIG_FILE = ROOT / "config.yaml"
LOG_DIR = ROOT / "logs"


def load_config() -> dict[str, Any]:
    """Loe config.yaml või kasuta vaikeseadeid, kui faili pole."""
    if not CONFIG_FILE.exists():
        return {
            "date_filter": {"start_date": None, "end_date": None},
            "pipeline": {
                "page_size": 1000,
                "max_retries": 3,
                "reference_date": "2025-02-28",
                "output_dir": "output",
                "use_sample_if_api_missing": True,
            },
        }
    return yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))


def apply_cli_date(config: dict[str, Any], analysis_date: str | None) -> dict[str, Any]:
    """Kasuta --date väärtust nii API filtris kui RFM võrdluskuupäevana."""
    if not analysis_date:
        return config

    pd.to_datetime(analysis_date, format="%Y-%m-%d")
    config.setdefault("date_filter", {})["end_date"] = analysis_date
    config.setdefault("pipeline", {})["reference_date"] = analysis_date
    return config


def setup_logging() -> None:
    """Seadista logimine nii terminali kui logs/ kausta failina."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"pipeline_{time.strftime('%Y%m%d')}.log"
    error_log_file = LOG_DIR / f"pipeline_errors_{time.strftime('%Y%m%d')}.log"
    error_handler = logging.FileHandler(error_log_file, encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_file, encoding="utf-8"), error_handler],
        force=True,
    )


def extract(config: dict[str, Any]) -> tuple[Any, Any, Any]:
    """Lae API-st sales/customers/products või kasuta varuandmeid."""
    logger = logging.getLogger(__name__)
    logger.info("[EXTRACT] start")

    pipeline_config = config["pipeline"]
    date_filter = config["date_filter"]
    table_config = config.get("tables", {})

    try:
        supabase = create_supabase_client()
        sales = fetch_sales(
            supabase,
            start_date=date_filter.get("start_date"),
            end_date=date_filter.get("end_date"),
            page_size=pipeline_config.get("page_size", 1000),
            max_retries=pipeline_config.get("max_retries", 3),
            table_name=table_config.get("sales", "sales"),
        )
        customers = fetch_customers(
            supabase,
            page_size=pipeline_config.get("page_size", 1000),
            max_retries=pipeline_config.get("max_retries", 3),
            table_name=table_config.get("customers", "customers"),
        )
        products = fetch_products(
            supabase,
            page_size=pipeline_config.get("page_size", 1000),
            max_retries=pipeline_config.get("max_retries", 3),
            table_name=table_config.get("products", "products"),
        )
        logger.info("[EXTRACT] done: sales=%s customers=%s products=%s", len(sales), len(customers), len(products))
        return sales, customers, products
    except Exception:
        logger.exception("[EXTRACT] Supabase API ebaonnestus")
        if pipeline_config.get("use_sample_if_api_missing", True):
            logger.warning("[EXTRACT] Kasutan varu-naidisandmeid, et pipeline jookseks lopuni")
            return sample_data()
        raise


def transform_data(sales: Any, customers: Any, products: Any, config: dict[str, Any]) -> dict[str, Any]:
    """Puhasta, filtreeri ja teisenda andmed raportite jaoks sobivaks."""
    logger = logging.getLogger(__name__)
    logger.info("[TRANSFORM] start")
    merged = merge_datasets(sales, customers, products)
    clean = clean_data(merged)
    before_cutoff = len(clean)
    reference_date = config["pipeline"].get("reference_date")
    if reference_date:
        cutoff = pd.to_datetime(reference_date)
        clean = clean[clean["sale_date"] <= cutoff].copy()
    period_start = clean["sale_date"].min().date() if not clean.empty else "puudub"
    period_end = clean["sale_date"].max().date() if not clean.empty else "puudub"
    period_label = f"andmebaasi algusest kuni {reference_date}" if reference_date else "kogu saadaolev periood"
    logger.info(
        "[TRANSFORM] Periood %s: %s -> %s rida; tegelik vahemik %s kuni %s",
        period_label,
        before_cutoff,
        len(clean),
        period_start,
        period_end,
    )
    weekly = calculate_weekly_aggregates(clean)
    kpis = calculate_kpis(clean)
    rfm = calculate_rfm(clean, reference_date=reference_date)
    segment_summary = calculate_segment_summary(rfm)
    interpretation = build_business_interpretation(rfm)
    logger.info("[TRANSFORM] done: rows=%s customers=%s", len(clean), kpis["unique_customers"])
    return {
        "clean_sales": clean,
        "weekly": weekly,
        "kpis": kpis,
        "rfm": rfm,
        "segment_summary": segment_summary,
        "business_interpretation": interpretation,
    }


def validate_results(results: dict[str, Any]) -> None:
    """Kontrolli, et pipeline'i peamised tulemused on olemas ja summad klapivad."""
    logger = logging.getLogger(__name__)
    logger.info("[VALIDATE] start")
    checks = {
        "clean_sales_not_empty": not results["clean_sales"].empty,
        "weekly_not_empty": not results["weekly"].empty,
        "rfm_not_empty": not results["rfm"].empty,
        "revenue_matches": round(results["clean_sales"]["total_price"].sum(), 2)
        == round(results["rfm"]["monetary_value"].sum(), 2),
    }
    for name, ok in checks.items():
        logger.info("[VALIDATE] %s: %s", name, "OK" if ok else "PROBLEEM")
    if not all(checks.values()):
        raise RuntimeError("Pipeline'i valideerimine ebaonnestus.")


def notify(
    status: str,
    summary: dict[str, Any],
    elapsed_seconds: float | None = None,
    output_dir: Path | None = None,
) -> None:
    """Saada valikuline emaili või webhooki teavitus pipeline'i tulemusega."""
    send_pipeline_notification(
        status=status,
        summary=summary,
        pipeline_name="Week 8 tiimitöö pipeline",
        elapsed_seconds=elapsed_seconds,
        output_dir=str(output_dir) if output_dir else None,
    )


def run_pipeline(analysis_date: str | None = None) -> dict[str, Any]:
    """Käivita kogu Week 8 tiimitöö pipeline algusest lõpuni."""
    logger = logging.getLogger(__name__)
    config = apply_cli_date(load_config(), analysis_date)
    start_time = time.perf_counter()

    try:
        logger.info("Pipeline started")
        sales, customers, products = extract(config)
        results = transform_data(sales, customers, products, config)
        validate_results(results)
        output_dir = ROOT / config["pipeline"].get("output_dir", "output")
        paths = export_results(results, output_dir=output_dir)
        elapsed = time.perf_counter() - start_time
        notify("SUCCESS", results["kpis"], elapsed_seconds=elapsed, output_dir=output_dir)
        logger.info("Pipeline complete %.2f seconds, files=%s", elapsed, len(paths))
        print(f"Pipeline valmis {elapsed:.2f} sekundiga. Väljundid: {output_dir}")
        reference_date = config["pipeline"].get("reference_date")
        period_label = f"andmebaasi algusest kuni {reference_date}" if reference_date else "kogu saadaolev periood"
        print(f"Analüüsi periood: {period_label}")
        print(results["segment_summary"].to_string(index=False))
        return results
    except Exception:
        logger.exception("Pipeline failed")
        notify("FAILED", {}, elapsed_seconds=time.perf_counter() - start_time)
        raise


def parse_args() -> argparse.Namespace:
    """Loe käsurealt analüüsi kuupäev, nt: python pipeline.py --date 2025-03-01."""
    parser = argparse.ArgumentParser(description="Week 8 team API pipeline")
    parser.add_argument(
        "--date",
        help="Valikuline analüüsi lõppkuupäev formaadis YYYY-MM-DD. Kui puudub, kasutatakse kõiki müügiridu.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    setup_logging()
    run_pipeline(analysis_date=args.date)
