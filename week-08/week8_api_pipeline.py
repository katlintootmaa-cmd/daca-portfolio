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
OUTPUT_DIR = ROOT / "output"
LOG_FILE = ROOT / "week8_pipeline.log"


def setup_logging() -> logging.Logger:
    """Configureeri logimine nii terminali kui faili."""
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

    return logger


logger = setup_logging()


def get_supabase_client() -> Any | None:
    """Loo Supabase Python client .env faili muutujate põhjal."""
    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY")

    if not url or not key:
        logger.warning("SUPABASE_URL ja/või SUPABASE_KEY puudub. Kasutan näidisandmeid.")
        return None

    return create_client(url, key)


def fetch_table(supabase: Any, table_name: str, page_size: int = 1000) -> pd.DataFrame:
    """Too kogu tabel Supabase API kaudu lehekülgede kaupa."""
    try:
        rows: list[dict[str, Any]] = []
        start = 0

        while True:
            end = start + page_size - 1
            response = supabase.table(table_name).select("*").range(start, end).execute()
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


def sample_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Loo juhendi struktuurile vastavad näidisandmed."""
    orders = pd.DataFrame(
        {
            "sale_id": range(1, 21),
            "customer_id": [
                1001,
                1002,
                1003,
                1001,
                1002,
                1004,
                1003,
                1001,
                1005,
                1004,
                1002,
                1003,
                1005,
                1001,
                1006,
                1004,
                1002,
                1007,
                1003,
                1005,
            ],
            "sale_date": pd.date_range("2024-01-15", periods=20, freq="10D"),
            "total_price": [
                89.99,
                45.50,
                120.00,
                67.30,
                55.00,
                210.00,
                33.50,
                145.00,
                78.00,
                92.00,
                160.00,
                44.00,
                88.50,
                230.00,
                37.00,
                175.00,
                110.00,
                65.00,
                95.00,
                125.00,
            ],
            "city": [
                "Tallinn",
                "Tartu",
                "Tallinn",
                "Tallinn",
                "Tartu",
                "Parnu",
                "Tallinn",
                "Tallinn",
                "Tartu",
                "Parnu",
                "Tartu",
                "Tallinn",
                "Tartu",
                "Tallinn",
                "Parnu",
                "Parnu",
                "Tartu",
                "Tallinn",
                "Tallinn",
                "Tartu",
            ],
        }
    )
    customers = pd.DataFrame(
        {
            "customer_id": [1001, 1002, 1003, 1004, 1005, 1006, 1007],
            "first_name": ["Juri", "Kati", "Maris", "Peeter", "Liina", "Andres", "Tiina"],
            "last_name": ["Tamm", "Kask", "Sepp", "Rebane", "Ots", "Puu", "Kuusk"],
            "city": ["Tallinn", "Tartu", "Tallinn", "Parnu", "Tartu", "Parnu", "Tallinn"],
        }
    )
    logger.info("Näidisandmed loodud: %s tellimust, %s klienti", len(orders), len(customers))
    return orders, customers


def extract(use_sample: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    """EXTRACT: too müügi- ja kliendiandmed API-st või näidisandmetest."""
    logger.info("[EXTRACT] Alustan")

    if use_sample:
        return sample_data()

    supabase = get_supabase_client()
    if supabase is None:
        return sample_data()

    orders = fetch_table(supabase, "sales")
    customers = fetch_table(supabase, "customers")

    if orders.empty or customers.empty:
        logger.warning("API andmed olid puudulikud. Kasutan kontrollitavat näidisandmestikku.")
        return sample_data()

    return orders, customers


def normalize_orders(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """Ühtlusta veerud, et pipeline töötaks nii API kui näidisandmetega."""
    df = orders.copy()
    customer_df = customers.copy()

    if "total_price" not in df.columns and "totalprice" in df.columns:
        df = df.rename(columns={"totalprice": "total_price"})

    if "sale_date" not in df.columns and "date" in df.columns:
        df = df.rename(columns={"date": "sale_date"})

    if "city" not in df.columns:
        if "store_location" in df.columns:
            df["city"] = df["store_location"].fillna("Online")
        elif "city" in customer_df.columns:
            df = df.merge(customer_df[["customer_id", "city"]], on="customer_id", how="left")
        else:
            df["city"] = "Teadmata"

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

    logger.info("[TRANSFORM] Puhastatud müügiridu: %s", len(df))
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


def assign_segment(score: int) -> str:
    """Määra lihtsustatud RFM segment koondskoori põhjal."""
    if score >= 8:
        return "VIP Champions"
    if score >= 6:
        return "Loyal Customers"
    if score >= 4:
        return "Potential Loyalists"
    return "At Risk"


def calculate_rfm(df: pd.DataFrame, reference_date: str | None = None) -> pd.DataFrame:
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

    rfm = (
        recency[["customer_id", "last_purchase", "recency_days"]]
        .merge(frequency, on="customer_id")
        .merge(monetary, on="customer_id")
    )

    unique_customers = len(rfm)
    q = min(3, unique_customers)
    if q < 2:
        rfm["R_score"] = 3
        rfm["F_score"] = 3
        rfm["M_score"] = 3
    else:
        rfm["R_score"] = pd.qcut(
            rfm["recency_days"].rank(method="first"), q=q, labels=range(q, 0, -1)
        ).astype(int)
        rfm["F_score"] = pd.qcut(
            rfm["frequency"].rank(method="first"), q=q, labels=range(1, q + 1)
        ).astype(int)
        rfm["M_score"] = pd.qcut(
            rfm["monetary"].rank(method="first"), q=q, labels=range(1, q + 1)
        ).astype(int)

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


def transform(orders: pd.DataFrame, customers: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """TRANSFORM: puhasta andmed ning loo raportid."""
    logger.info("[TRANSFORM] Alustan")
    clean_orders = normalize_orders(orders, customers)

    reports = pd.DataFrame([city_report(clean_orders, city) for city in sorted(clean_orders["city"].dropna().unique())])
    weekly = pd.DataFrame([weekly_sales_report(clean_orders)])
    rfm = calculate_rfm(clean_orders)
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
        hover_data=["customer_id", "RFM_score"],
        title="UrbanStyle RFM kliendisegmendid",
        labels={"recency_days": "Päevi viimasest ostust", "monetary": "Kogukulutus (EUR)"},
    ).write_html(rfm_chart_path)

    px.bar(
        results["monthly"],
        x="sale_date",
        y="revenue",
        title="UrbanStyle kuukäive",
        labels={"sale_date": "Kuu", "revenue": "Käive (EUR)"},
        text="revenue",
    ).write_html(monthly_chart_path)

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
        rfm[["customer_id", "frequency", "monetary", "recency_days", "RFM_score", "segment"]]
        .head(20)
        .to_string(index=False)
    )
    if len(rfm) > 20:
        print(f"... kokku segmenteeritud kliente: {len(rfm)}")

    best_customer = rfm.sort_values("monetary", ascending=False).iloc[0]
    best_month = monthly.sort_values("revenue", ascending=False).iloc[0]

    print("\n--- VASTUSED ---")
    print(f"RFM segmentide arv: {rfm['segment'].nunique()}")
    print(f"Kõige väärtuslikum klient: {int(best_customer['customer_id'])}, monetary {best_customer['monetary']:.2f} EUR")
    print(f"Kõige kasumlikum kuu: {best_month['sale_date']}, käive {best_month['revenue']:.2f} EUR")


def run_pipeline(use_sample: bool = False) -> dict[str, pd.DataFrame]:
    """Käivita kogu ETL pipeline."""
    started_at = datetime.now()
    logger.info("MARKO IGANÄDALANE RFM PIPELINE")

    orders, customers = extract(use_sample=use_sample)
    results = transform(orders, customers)

    if validate(results):
        load(results)
    else:
        raise RuntimeError("Valideerimine ebaõnnestus. LOAD etappi ei käivitatud.")

    logger.info("Pipeline valmis %.1f sekundiga", (datetime.now() - started_at).total_seconds())
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Week 8 API ja RFM ETL pipeline")
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Kasuta Supabase API asemel juhendi näidisandmeid.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = run_pipeline(use_sample=args.sample)
    print_summary(results)


if __name__ == "__main__":
    main()
