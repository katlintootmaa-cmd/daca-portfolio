"""Week 8 API pipeline demo.

See skript laeb UrbanStyle müügi- ja kliendiandmed Supabase API-st,
kasutab vajadusel CSV fallbacki, puhastab andmed, arvutab KPI-d ja RFM
segmendid ning salvestab raportid CSV/HTML failidena.

Märkus: see fail on individuaalne demo-/arhiiviversioon.
Põhiline hooldatav Week 8 pipeline asub failis week-08/team/pipeline.py.
"""

from __future__ import annotations

import argparse
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from supabase import create_client


ROOT = Path(__file__).resolve().parent
WEEK_ROOT = ROOT.parent
PROJECT_ROOT = WEEK_ROOT.parent
OUTPUT_DIR = ROOT / "output"
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "week8_pipeline.log"
ERROR_LOG_FILE = LOG_DIR / "week8_pipeline_errors.log"

# Vaikimisi kasutatakse Week 7 RFM tööga sama analüüsi lõppkuupäeva.
# Kui tahad analüüsi teise kuupäevani piirata, anna CLI-s --date YYYY-MM-DD.
ANALYSIS_END_DATE: str | None = "2025-02-28"

# Kohalikud CSV failid, mida kasutatakse siis, kui API ei ole saadaval.
FALLBACK_SALES_PATHS = [
    PROJECT_ROOT / "datasets" / "clean" / "sales.csv",
    WEEK_ROOT / "datasets" / "clean" / "sales.csv",
    PROJECT_ROOT / "SQL" / "sales_supabase_import.csv",
    PROJECT_ROOT / "SQL" / "sales_rows.csv",
]
FALLBACK_CUSTOMER_PATHS = [
    PROJECT_ROOT / "datasets" / "clean" / "customers.csv",
    WEEK_ROOT / "datasets" / "clean" / "customers.csv",
    PROJECT_ROOT / "SQL" / "customers.csv",
    PROJECT_ROOT / "SQL" / "customers_rows.csv",
]


def setup_logging() -> logging.Logger:
    """Configureeri logimine nii terminali kui faili."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("week8_pipeline")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    error_handler = logging.FileHandler(ERROR_LOG_FILE, encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    return logger


logger = setup_logging()


def get_supabase_client() -> Any | None:
    """Loo Supabase Python client .env faili muutujate põhjal."""
    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY")

    if not url or not key:
        logger.warning("SUPABASE_URL ja/või SUPABASE_KEY puudub. Proovin CSV fallbacki.")
        return None

    return create_client(url, key)


def fetch_table(
    supabase: Any,
    table_name: str,
    page_size: int = 1000,
    date_column: str | None = None,
    end_date: str | None = None,
) -> pd.DataFrame:
    """Too kogu tabel Supabase API kaudu lehekülgede kaupa."""
    try:
        rows: list[dict[str, Any]] = []
        start = 0

        while True:
            end = start + page_size - 1
            query = supabase.table(table_name).select("*")
            if date_column and end_date:
                query = query.lte(date_column, end_date)
            response = query.range(start, end).execute()
            page = response.data or []
            rows.extend(page)
            logger.info(
                "Tabel '%s': laaditud read %s-%s, lehel %s rida",
                table_name,
                start,
                end,
                len(page),
            )

            if len(page) < page_size:
                break

            start += page_size

        df = pd.DataFrame(rows)
        logger.info("Laaditud tabel '%s': %s rida", table_name, len(df))
        return df
    except Exception as exc:
        logger.error("Tabeli '%s' laadimine ebaõnnestus: %s", table_name, exc)
        return pd.DataFrame()


def read_first_existing_csv(paths: list[Path], label: str) -> pd.DataFrame:
    """Loe esimene olemasolev fallback CSV fail."""
    for path in paths:
        if path.exists():
            df = pd.read_csv(path)
            logger.info("Fallback CSV '%s': %s rida failist %s", label, len(df), path)
            return df

    logger.warning("Fallback CSV '%s' puudub. Otsitud failid: %s", label, ", ".join(str(path) for path in paths))
    return pd.DataFrame()


def fallback_csv_data() -> tuple[pd.DataFrame, pd.DataFrame] | None:
    """Fallback: kasuta kohalikke CSV faile, kui API ei ole saadaval."""
    orders = read_first_existing_csv(FALLBACK_SALES_PATHS, "sales")
    if orders.empty:
        return None

    customers = read_first_existing_csv(FALLBACK_CUSTOMER_PATHS, "customers")
    print(f"Fallback CSV: {len(orders)} sales rows")
    if not customers.empty:
        print(f"Fallback CSV: {len(customers)} customer rows")

    return orders, customers


def extract(analysis_date: str | None = ANALYSIS_END_DATE) -> tuple[pd.DataFrame, pd.DataFrame]:
    """EXTRACT: too müügi- ja kliendiandmed API-st või CSV fallbackist."""
    logger.info("[EXTRACT] Alustan")

    supabase = get_supabase_client()
    if supabase is None:
        fallback = fallback_csv_data()
        if fallback is None:
            raise RuntimeError("API ei ole seadistatud ja fallback CSV faile ei leitud.")
        return fallback

    orders = fetch_table(supabase, "sales", date_column="sale_date", end_date=analysis_date)
    customers = fetch_table(supabase, "customers")

    if orders.empty or customers.empty:
        logger.warning("API andmed olid puudulikud. Proovin fallback CSV faile.")
        fallback = fallback_csv_data()
        if fallback is None:
            raise RuntimeError("API andmed olid puudulikud ja fallback CSV faile ei leitud.")
        return fallback

    return orders, customers


def normalize_orders(
    orders: pd.DataFrame,
    customers: pd.DataFrame,
    analysis_date: str | None = ANALYSIS_END_DATE,
) -> pd.DataFrame:
    """Ühtlusta veerud, et pipeline töötaks nii API kui CSV andmetega."""
    df = orders.copy()
    customer_df = customers.copy()

    if "total_price" not in df.columns and "totalprice" in df.columns:
        df = df.rename(columns={"totalprice": "total_price"})

    if "sale_date" not in df.columns and "date" in df.columns:
        df = df.rename(columns={"date": "sale_date"})

    # Toome klienditabelist nime ja kontaktid müügiridade juurde.
    customer_columns = [
        column
        for column in ["customer_id", "first_name", "last_name", "email", "phone", "city"]
        if column in customer_df.columns
    ]
    if len(customer_columns) > 1:
        customer_lookup = customer_df[customer_columns].drop_duplicates("customer_id")
        df = df.merge(customer_lookup, on="customer_id", how="left", suffixes=("", "_customer"))

    if "city" not in df.columns:
        if "store_location" in df.columns:
            df["city"] = df["store_location"].fillna("Online")
        elif "city_customer" in df.columns:
            df["city"] = df["city_customer"]
        else:
            df["city"] = "Teadmata"
    elif "city_customer" in df.columns:
        df["city"] = df["city"].fillna(df["city_customer"])

    for column in ["first_name", "last_name"]:
        if column not in df.columns:
            df[column] = ""
    for column in ["email", "phone"]:
        if column not in df.columns:
            df[column] = ""
    df["customer_name"] = (
        df["first_name"].fillna("").astype(str).str.strip()
        + " "
        + df["last_name"].fillna("").astype(str).str.strip()
    ).str.strip()
    df.loc[df["customer_name"] == "", "customer_name"] = "Klient " + df["customer_id"].astype(str)
    # Analüüsi jäävad ainult kliendid, kellel on e-mail või telefon olemas.
    df["has_email"] = df["email"].notna() & (df["email"].astype(str).str.strip() != "")
    df["has_phone"] = df["phone"].notna() & (df["phone"].astype(str).str.strip() != "")
    df["has_contact"] = df["has_email"] | df["has_phone"]

    required = ["customer_id", "sale_date", "total_price", "city"]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Puuduvad kohustuslikud veerud: {', '.join(missing)}")

    df = df.dropna(subset=["customer_id", "sale_date", "total_price"]).copy()
    df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
    df["total_price"] = pd.to_numeric(df["total_price"], errors="coerce")
    df = df.dropna(subset=["sale_date", "total_price"])
    df = df[df["total_price"] > 0]
    df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["customer_id"])
    before_cutoff = len(df)
    if analysis_date is not None:
        cutoff = pd.to_datetime(analysis_date)
        df = df[df["sale_date"] <= cutoff].copy()
    before_contact_filter = len(df)
    df = df[df["has_contact"]].copy()
    period_label = f"andmebaasi algusest kuni {analysis_date}" if analysis_date else "kogu saadaolev periood"

    logger.info(
        "[TRANSFORM] Periood %s: kuupäevafilter %s -> %s; kontaktifilter %s -> %s; tegelik vahemik %s kuni %s",
        period_label,
        before_cutoff,
        before_contact_filter,
        before_contact_filter,
        len(df),
        df["sale_date"].min().date() if not df.empty else "puudub",
        df["sale_date"].max().date() if not df.empty else "puudub",
    )
    return df


def city_report(df: pd.DataFrame, city: str) -> dict[str, Any]:
    """Arvuta ühe linna tellimuste arv, kogukäive ja keskmine tellimus."""
    city_data = df[df["city"] == city]
    return {
        "city": city,
        "orders": len(city_data),
        "revenue": round(city_data["total_price"].sum(), 2),
        "avg_order": round(city_data["total_price"].mean(), 2) if len(city_data) else 0.0,
    }


def weekly_sales_report(df: pd.DataFrame, report_date: str | None = None) -> dict[str, Any]:
    """Genereeri iganädalane müügiraport."""
    if report_date is None:
        report_date = datetime.now().strftime("%Y-%m-%d")

    return {
        "report_date": report_date,
        "total_orders": len(df),
        "total_revenue": round(df["total_price"].sum(), 2),
        "avg_order": round(df["total_price"].mean(), 2) if len(df) else 0.0,
        "unique_customers": int(df["customer_id"].nunique()),
    }


def score_column(series: pd.Series, labels: list[int]) -> pd.Series:
    """Jaga väärtused kuni viide kvantiili ja teisenda need R/F/M skooriks."""
    q = min(5, series.nunique())
    if q < 2:
        return pd.Series([max(labels)] * len(series), index=series.index, dtype="int64")
    return pd.qcut(series.rank(method="first"), q=q, labels=labels[:q]).astype(int)


def assign_segment(score: int) -> str:
    """Määra lihtsustatud RFM segment koondskoori põhjal."""
    if score >= 13:
        return "VIP Champions"
    if score >= 10:
        return "Loyal"
    if score >= 7:
        return "Potential"
    if score >= 4:
        return "At Risk"
    return "Lost"


def calculate_rfm(df: pd.DataFrame, reference_date: str | None = ANALYSIS_END_DATE) -> pd.DataFrame:
    """Arvuta RFM skoorid ja segmendid iga kliendi kohta."""
    if df.empty:
        return pd.DataFrame()

    if reference_date is None:
        ref = df["sale_date"].max() + pd.Timedelta(days=1)
    else:
        ref = pd.to_datetime(reference_date)

    rfm_source = df.copy()

    recency = rfm_source.groupby("customer_id")["sale_date"].max().reset_index()
    recency.columns = ["customer_id", "last_purchase"]
    recency["recency_days"] = (ref - recency["last_purchase"]).dt.days

    frequency = rfm_source.groupby("customer_id").size().reset_index(name="frequency")
    monetary = rfm_source.groupby("customer_id")["total_price"].sum().reset_index()
    monetary.columns = ["customer_id", "monetary"]
    names = rfm_source.groupby("customer_id")["customer_name"].first().reset_index()
    contacts = (
        rfm_source.groupby("customer_id")
        .agg(has_email=("has_email", "max"), has_phone=("has_phone", "max"), has_contact=("has_contact", "max"))
        .reset_index()
    )

    rfm = (
        recency[["customer_id", "last_purchase", "recency_days"]]
        .merge(frequency, on="customer_id")
        .merge(monetary, on="customer_id")
        .merge(names, on="customer_id", how="left")
        .merge(contacts, on="customer_id", how="left")
    )

    rfm["R_score"] = score_column(rfm["recency_days"], [5, 4, 3, 2, 1])
    rfm["F_score"] = score_column(rfm["frequency"], [1, 2, 3, 4, 5])
    rfm["M_score"] = score_column(rfm["monetary"], [1, 2, 3, 4, 5])

    # Koondskoor määrab, millisesse turundussegmenti klient kuulub.
    rfm["RFM_score"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]
    rfm["segment"] = rfm["RFM_score"].apply(assign_segment)
    return rfm.sort_values(["RFM_score", "monetary"], ascending=False)


def monthly_report(df: pd.DataFrame) -> pd.DataFrame:
    """Arvuta kuukäive ja tellimuste arv."""
    monthly = (
        df.groupby(df["sale_date"].dt.to_period("M"))
        .agg(orders=("sale_date", "count"), revenue=("total_price", "sum"))
        .reset_index()
    )
    monthly["sale_date"] = monthly["sale_date"].astype(str)
    monthly["revenue"] = monthly["revenue"].round(2)
    return monthly


def transform(
    orders: pd.DataFrame,
    customers: pd.DataFrame,
    analysis_date: str | None = ANALYSIS_END_DATE,
) -> dict[str, pd.DataFrame]:
    """TRANSFORM: puhasta andmed ning loo raportid."""
    logger.info("[TRANSFORM] Alustan")
    clean_orders = normalize_orders(orders, customers, analysis_date=analysis_date)

    reports = pd.DataFrame([city_report(clean_orders, city) for city in sorted(clean_orders["city"].dropna().unique())])
    weekly = pd.DataFrame([weekly_sales_report(clean_orders)])
    rfm = calculate_rfm(clean_orders, reference_date=analysis_date)
    monthly = monthly_report(clean_orders)

    logger.info("[TRANSFORM] RFM segmente: %s", rfm["segment"].nunique() if not rfm.empty else 0)
    return {"orders": clean_orders, "city": reports, "weekly": weekly, "rfm": rfm, "monthly": monthly}


def validate(results: dict[str, pd.DataFrame]) -> bool:
    """VALIDATE: kontrolli, et pipeline'i tulemused on kasutatavad."""
    logger.info("[VALIDATE] Kontrollin tulemusi")

    checks = {
        "orders_not_empty": not results["orders"].empty,
        "rfm_not_empty": not results["rfm"].empty,
        "revenue_positive": results["orders"]["total_price"].sum() > 0,
        "monthly_matches_total": round(results["monthly"]["revenue"].sum(), 2)
        == round(results["orders"]["total_price"].sum(), 2),
    }

    for check, ok in checks.items():
        logger.info("[VALIDATE] %s: %s", check, "OK" if ok else "PROBLEEM")

    return all(checks.values())


def load(results: dict[str, pd.DataFrame]) -> None:
    """LOAD: salvesta CSV raportid ja Plotly HTML graafikud."""
    logger.info("[LOAD] Salvestan väljundid")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    rfm_path = OUTPUT_DIR / f"rfm_report_{timestamp}.csv"
    city_path = OUTPUT_DIR / f"city_report_{timestamp}.csv"
    monthly_path = OUTPUT_DIR / f"monthly_report_{timestamp}.csv"
    rfm_chart_path = OUTPUT_DIR / f"rfm_chart_{timestamp}.html"
    monthly_chart_path = OUTPUT_DIR / f"monthly_chart_{timestamp}.html"

    results["rfm"].to_csv(rfm_path, index=False)
    results["city"].to_csv(city_path, index=False)
    results["monthly"].to_csv(monthly_path, index=False)

    px.scatter(
        results["rfm"],
        x="recency_days",
        y="monetary",
        color="segment",
        size="frequency",
        hover_data=["customer_name", "RFM_score"],
        title="UrbanStyle RFM kliendisegmendid",
        labels={"recency_days": "Päevi viimasest ostust", "monetary": "Kogukulutus (EUR)"},
    ).write_html(rfm_chart_path)

    px.line(
        results["monthly"],
        x="sale_date",
        y="revenue",
        title="UrbanStyle kuukäive",
        labels={"sale_date": "Kuu", "revenue": "Käive (EUR)"},
        markers=True,
    ).update_traces(line={"width": 3}, marker={"size": 8}).write_html(monthly_chart_path)

    logger.info("[LOAD] CSV ja HTML väljundid salvestatud kausta %s", OUTPUT_DIR)


def print_summary(results: dict[str, pd.DataFrame]) -> None:
    """Prindi juhendi küsimustele sobiv kokkuvõte."""
    weekly = results["weekly"].iloc[0].to_dict()
    rfm = results["rfm"]
    monthly = results["monthly"]

    print("\n--- IGANÄDALANE RAPORT ---")
    for key, value in weekly.items():
        print(f"{key}: {value}")

    print("\n--- LINNADE RAPORT ---")
    print(results["city"].sort_values("revenue", ascending=False).to_string(index=False))

    print("\n--- RFM SEGMENDID: TOP 20 ---")
    print(
        rfm[
            [
                "customer_name",
                "frequency",
                "monetary",
                "recency_days",
                "RFM_score",
                "segment",
            ]
        ]
        .head(20)
        .to_string(index=False)
    )
    if len(rfm) > 20:
        print(f"... kokku segmenteeritud kliente: {len(rfm)}")

    best_customer = rfm.sort_values("monetary", ascending=False).iloc[0]
    best_month = monthly.sort_values("revenue", ascending=False).iloc[0]

    print("\n--- VASTUSED ---")
    print(f"RFM segmentide arv: {rfm['segment'].nunique()}")
    print(f"Kõige väärtuslikum klient: {best_customer['customer_name']}, monetary {best_customer['monetary']:.2f} EUR")
    print(f"Kõige kasumlikum kuu: {best_month['sale_date']}, käive {best_month['revenue']:.2f} EUR")


def run_pipeline(
    analysis_date: str | None = ANALYSIS_END_DATE,
) -> dict[str, pd.DataFrame]:
    """Käivita kogu ETL pipeline."""
    if analysis_date is not None:
        pd.to_datetime(analysis_date, format="%Y-%m-%d")
    started_at = datetime.now()
    if analysis_date is None:
        logger.info("MARKO IGANÄDALANE RFM PIPELINE kogu saadaoleva perioodi kohta")
    else:
        logger.info("MARKO IGANÄDALANE RFM PIPELINE kuni %s", analysis_date)

    orders, customers = extract(analysis_date=analysis_date)
    results = transform(orders, customers, analysis_date=analysis_date)

    if validate(results):
        load(results)
    else:
        raise RuntimeError("Valideerimine ebaõnnestus. LOAD etappi ei käivitatud.")

    logger.info("Pipeline valmis %.1f sekundiga", (datetime.now() - started_at).total_seconds())
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Week 8 API ja RFM ETL pipeline")
    parser.add_argument(
        "--date",
        default=ANALYSIS_END_DATE,
        help=(
            "Valikuline analüüsi lõppkuupäev formaadis YYYY-MM-DD. "
            "Kui puudub, kasutatakse kõiki müügiridu."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        results = run_pipeline(analysis_date=args.date)
        print_summary(results)
    except Exception:
        logger.exception("Pipeline ebaõnnestus")
        raise


if __name__ == "__main__":
    main()
