"""Roll B: Data Processing.

See moodul puhastab API-st tulnud andmed, ühendab müügi-, kliendi- ja
tooteandmed, arvutab nädalased koondnäitajad, KPI-d ning RFM segmendid.
"""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd


logger = logging.getLogger(__name__)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Eemalda vigased read ja lisa kontaktide kontrolliks abiveerud."""
    required = {"customer_id", "sale_date", "total_price"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"Puuduvad kohustuslikud veerud: {', '.join(missing)}")

    before = len(df)
    clean = df.drop_duplicates().copy()
    clean["sale_date"] = pd.to_datetime(clean["sale_date"], errors="coerce")
    clean["customer_id"] = pd.to_numeric(clean["customer_id"], errors="coerce")
    clean["total_price"] = pd.to_numeric(clean["total_price"], errors="coerce")
    clean = clean.dropna(subset=["customer_id", "sale_date", "total_price"]).copy()
    clean = clean[clean["total_price"] > 0].copy()
    clean["customer_id"] = clean["customer_id"].astype(int)

    if "sale_id" not in clean.columns:
        clean["sale_id"] = range(1, len(clean) + 1)

    for column in ["email", "phone", "first_name", "last_name", "city", "loyalty_tier"]:
        if column not in clean.columns:
            clean[column] = pd.NA

    clean["has_email"] = clean["email"].notna() & (clean["email"].astype(str).str.strip() != "")
    clean["has_phone"] = clean["phone"].notna() & (clean["phone"].astype(str).str.strip() != "")
    clean["has_contact"] = clean["has_email"] | clean["has_phone"]

    logger.info("clean_data: %s -> %s rida", before, len(clean))
    return clean


def merge_datasets(
    df_sales: pd.DataFrame,
    df_customers: pd.DataFrame,
    df_products: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Ühenda müügiandmed kliendiandmetega ja võimalusel tooteandmetega."""
    if "customer_id" not in df_sales.columns or "customer_id" not in df_customers.columns:
        raise ValueError("Müügi- ja kliendiandmetes peab olema customer_id veerg.")

    merged = df_sales.merge(df_customers, on="customer_id", how="left", suffixes=("_sale", ""))

    if df_products is not None and not df_products.empty and "product_id" in merged.columns and "product_id" in df_products.columns:
        merged = merged.merge(df_products, on="product_id", how="left", suffixes=("", "_product"))

    if "city" not in merged.columns:
        merged["city"] = pd.NA
    if "store_location" in merged.columns:
        merged["city"] = merged["city"].fillna(merged["store_location"])
    if "channel" in merged.columns:
        merged.loc[merged["city"].isna() & (merged["channel"].astype(str).str.lower() == "online"), "city"] = "Online"
    merged["city"] = merged["city"].fillna("Teadmata")

    logger.info("merge_datasets: %s rida", len(merged))
    return merged


def calculate_weekly_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """Arvuta nädalate kaupa tulu, tellimuste arv ja unikaalsed kliendid."""
    weekly = (
        df.resample("W-MON", on="sale_date", label="left", closed="left")
        .agg(
            revenue=("total_price", "sum"),
            orders=("sale_id", "count"),
            unique_customers=("customer_id", "nunique"),
        )
        .reset_index()
        .rename(columns={"sale_date": "week"})
    )
    weekly["avg_order_value"] = weekly["revenue"] / weekly["orders"]
    weekly[["revenue", "avg_order_value"]] = weekly[["revenue", "avg_order_value"]].round(2)
    return weekly


def calculate_kpis(df: pd.DataFrame) -> dict[str, Any]:
    """Tagasta peamised juhtimisnäitajad ühe dict objektina."""
    orders = len(df)
    total_revenue = float(df["total_price"].sum())
    return {
        "total_revenue": round(total_revenue, 2),
        "orders": int(orders),
        "unique_customers": int(df["customer_id"].nunique()),
        "avg_order_value": round(total_revenue / orders, 2) if orders else 0.0,
    }


def calculate_city_report(df: pd.DataFrame) -> pd.DataFrame:
    """Arvuta linnade kaupa tellimuste arv, kogutulu ja keskmine tellimus."""
    city = (
        df.groupby("city")
        .agg(
            orders=("sale_id", "count"),
            revenue=("total_price", "sum"),
            avg_order_value=("total_price", "mean"),
            unique_customers=("customer_id", "nunique"),
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    city[["revenue", "avg_order_value"]] = city[["revenue", "avg_order_value"]].round(2)
    return city


def calculate_monthly_report(df: pd.DataFrame) -> pd.DataFrame:
    """Arvuta kuude kaupa tulu, tellimuste arv ja unikaalsed kliendid."""
    monthly = (
        df.groupby(df["sale_date"].dt.to_period("M"))
        .agg(
            orders=("sale_id", "count"),
            revenue=("total_price", "sum"),
            unique_customers=("customer_id", "nunique"),
        )
        .reset_index()
        .rename(columns={"sale_date": "month"})
    )
    monthly["month"] = monthly["month"].astype(str)
    monthly["avg_order_value"] = monthly["revenue"] / monthly["orders"]
    monthly[["revenue", "avg_order_value"]] = monthly[["revenue", "avg_order_value"]].round(2)
    return monthly


def _score_column(series: pd.Series, labels: list[int]) -> pd.Series:
    """Jaga väärtused kuni viide kvantiili ja teisenda need R/F/M skooriks."""
    q = min(5, series.nunique())
    if q < 2:
        return pd.Series([max(labels)] * len(series), index=series.index, dtype="int64")
    return pd.qcut(series.rank(method="first"), q, labels=labels[:q]).astype(int)


def assign_segment(score: int) -> str:
    """Määra RFM koondskoori põhjal turundussegment."""
    if score >= 13:
        return "VIP Champions"
    if score >= 10:
        return "Loyal"
    if score >= 7:
        return "Potential"
    if score >= 4:
        return "At Risk"
    return "Lost"


def calculate_rfm(df: pd.DataFrame, reference_date: str | None = None) -> pd.DataFrame:
    """Koonda andmed kliendi tasemele ning arvuta RFM skoorid ja segment."""
    today = pd.to_datetime(reference_date) if reference_date else df["sale_date"].max() + pd.Timedelta(days=1)
    rfm = (
        df.groupby("customer_id")
        .agg(
            last_purchase_date=("sale_date", "max"),
            frequency=("sale_id", "count"),
            monetary_value=("total_price", "sum"),
            first_name=("first_name", "first"),
            last_name=("last_name", "first"),
            email=("email", "first"),
            phone=("phone", "first"),
            has_email=("has_email", "max"),
            has_phone=("has_phone", "max"),
            has_contact=("has_contact", "max"),
            city=("city", "first"),
            loyalty_tier=("loyalty_tier", "first"),
        )
        .reset_index()
    )
    rfm["recency_days"] = (today - rfm["last_purchase_date"]).dt.days
    rfm["R_score"] = _score_column(rfm["recency_days"], [5, 4, 3, 2, 1])
    rfm["F_score"] = _score_column(rfm["frequency"], [1, 2, 3, 4, 5])
    rfm["M_score"] = _score_column(rfm["monetary_value"], [1, 2, 3, 4, 5])
    rfm["RFM_Score"] = rfm[["R_score", "F_score", "M_score"]].sum(axis=1)
    rfm["Segment"] = rfm["RFM_Score"].apply(assign_segment)
    rfm["customer_name"] = (
        rfm["first_name"].fillna("").astype(str).str.strip()
        + " "
        + rfm["last_name"].fillna("").astype(str).str.strip()
    ).str.strip()
    rfm.loc[rfm["customer_name"] == "", "customer_name"] = "Klient " + rfm["customer_id"].astype(str)
    return rfm.sort_values(["RFM_Score", "monetary_value"], ascending=False)


def calculate_segment_summary(rfm: pd.DataFrame) -> pd.DataFrame:
    """Tee segmentide lõikes kokkuvõte klientide arvu ja käibe kohta."""
    summary = (
        rfm.groupby("Segment")
        .agg(
            customers=("customer_id", "count"),
            avg_recency_days=("recency_days", "mean"),
            avg_frequency=("frequency", "mean"),
            total_revenue=("monetary_value", "sum"),
            avg_monetary_value=("monetary_value", "mean"),
            reachable_customers=("has_contact", "sum"),
        )
        .reset_index()
    )
    summary["customer_share_pct"] = summary["customers"] / summary["customers"].sum() * 100
    summary["revenue_share_pct"] = summary["total_revenue"] / summary["total_revenue"].sum() * 100
    summary["reachable_share_pct"] = summary["reachable_customers"] / summary["customers"] * 100
    return summary.sort_values("total_revenue", ascending=False).round(2)


def build_business_interpretation(rfm: pd.DataFrame) -> str:
    """Koosta Markole lühike tekstiline tõlgendus RFM tulemustest."""
    total_customers = int(rfm["customer_id"].nunique())
    total_revenue = rfm["monetary_value"].sum()
    vip_customers = int((rfm["Segment"] == "VIP Champions").sum())
    at_risk_customers = int((rfm["Segment"] == "At Risk").sum())
    lost_customers = int((rfm["Segment"] == "Lost").sum())
    vip_revenue = rfm.loc[rfm["Segment"] == "VIP Champions", "monetary_value"].sum()
    at_risk_revenue = rfm.loc[rfm["Segment"] == "At Risk", "monetary_value"].sum()
    vip_share = vip_revenue / total_revenue * 100 if total_revenue else 0
    at_risk_share = at_risk_revenue / total_revenue * 100 if total_revenue else 0

    return f"""# Week 8 tiimitöö API RFM raport

UrbanStyle andmestikus on {total_customers} analüüsitavat klienti, kellest {vip_customers} kuuluvad VIP Champions segmenti.
VIP kliendid annavad {vip_share:.1f}% kogukäibest.
At Risk segmendis on {at_risk_customers} klienti ja Lost segmendis {lost_customers} klienti.
At Risk segment annab veel {at_risk_share:.1f}% käibest.

## Soovitused Markole

1. VIP Champions: käivita early access programm, personaalsed pakkumised ja VIP sooduskoodid.
2. At Risk: saada win-back pakkumine enne, kui kliendid liiguvad Lost segmenti.
3. Potential ja Loyal: kasvata neid lojaalsusprogrammi ja cross-sell pakkumistega VIP segmendiks.
"""
