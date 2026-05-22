"""Roll B: Data processing for the Week 8 marketing pipeline."""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd


logger = logging.getLogger(__name__)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove invalid rows and add contact helper columns."""
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
    """Merge sales, customer and optional product data."""
    if "customer_id" not in df_sales.columns or "customer_id" not in df_customers.columns:
        raise ValueError("Muugi- ja kliendiandmetes peab olema customer_id veerg.")

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
    """Calculate weekly revenue, orders and unique customers."""
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
    iso_calendar = weekly["week"].dt.isocalendar()
    weekly["week_year"] = iso_calendar["year"].astype(int)
    weekly["week_number"] = iso_calendar["week"].astype(int)
    weekly["week_label"] = weekly["week_year"].astype(str) + " nädal " + weekly["week_number"].astype(str)
    weekly["avg_order_value"] = weekly["revenue"] / weekly["orders"]
    weekly[["revenue", "avg_order_value"]] = weekly[["revenue", "avg_order_value"]].round(2)
    return weekly


def calculate_kpis(df: pd.DataFrame) -> dict[str, Any]:
    """Return the main management KPIs."""
    orders = len(df)
    total_revenue = float(df["total_price"].sum())
    unique_customers = int(df["customer_id"].nunique())
    return {
        "total_revenue": round(total_revenue, 2),
        "orders": int(orders),
        "unique_customers": unique_customers,
        "avg_order_value": round(total_revenue / orders, 2) if orders else 0.0,
        "revenue_per_customer": round(total_revenue / unique_customers, 2) if unique_customers else 0.0,
    }


def calculate_data_quality_report(raw: pd.DataFrame, clean: pd.DataFrame) -> pd.DataFrame:
    """Create a simple before/after data quality report."""
    raw_total_price = (
        pd.to_numeric(raw["total_price"], errors="coerce") if "total_price" in raw.columns else pd.Series(dtype=float)
    )
    raw_sale_date = (
        pd.to_datetime(raw["sale_date"], errors="coerce") if "sale_date" in raw.columns else pd.Series(dtype="datetime64[ns]")
    )
    checks = [
        ("rows_before_cleaning", len(raw), "Sisendridade arv enne puhastamist"),
        ("rows_after_cleaning", len(clean), "Ridade arv pärast puhastamist"),
        ("rows_removed", len(raw) - len(clean), "Puhastamisel eemaldatud read"),
        ("duplicate_rows", int(raw.duplicated().sum()) if not raw.empty else 0, "Täielikud duplikaatread"),
        ("missing_customer_id", int(raw["customer_id"].isna().sum()) if "customer_id" in raw.columns else 0, "Puuduva customer_id-ga read"),
        ("invalid_sale_date", int(raw_sale_date.isna().sum()), "Puuduvad või vigased kuupäevad"),
        ("non_positive_revenue", int((raw_total_price <= 0).sum()), "Nullist väiksema või võrdse summaga read"),
        ("missing_contact_clean", int((~clean["has_contact"]).sum()) if "has_contact" in clean.columns else 0, "Puhastes andmetes kontaktita read"),
    ]
    return pd.DataFrame(checks, columns=["metric", "value", "description"])


def calculate_city_report(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate city-level orders, revenue and average order value."""
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


def calculate_channel_report(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate channel-level orders, revenue and average order value."""
    if "channel" not in df.columns:
        return pd.DataFrame(columns=["channel", "orders", "revenue", "avg_order_value", "unique_customers"])
    channel = (
        df.assign(channel=df["channel"].fillna("Teadmata"))
        .groupby("channel")
        .agg(
            orders=("sale_id", "count"),
            revenue=("total_price", "sum"),
            avg_order_value=("total_price", "mean"),
            unique_customers=("customer_id", "nunique"),
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    channel[["revenue", "avg_order_value"]] = channel[["revenue", "avg_order_value"]].round(2)
    return channel


def calculate_monthly_report(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly revenue, orders and unique customers."""
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


def calculate_cohort_retention(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate month-based retention cohorts from first purchase month."""
    cohort_df = df[["customer_id", "sale_date"]].copy()
    cohort_df["order_month"] = cohort_df["sale_date"].dt.to_period("M")
    first_purchase = cohort_df.groupby("customer_id")["order_month"].min().rename("cohort_month")
    cohort_df = cohort_df.merge(first_purchase, on="customer_id", how="left")
    cohort_df["cohort_index"] = (
        (cohort_df["order_month"].dt.year - cohort_df["cohort_month"].dt.year) * 12
        + (cohort_df["order_month"].dt.month - cohort_df["cohort_month"].dt.month)
    )
    cohorts = (
        cohort_df.groupby(["cohort_month", "cohort_index"])["customer_id"]
        .nunique()
        .reset_index(name="active_customers")
    )
    cohort_sizes = cohorts[cohorts["cohort_index"] == 0][["cohort_month", "active_customers"]].rename(
        columns={"active_customers": "cohort_size"}
    )
    cohorts = cohorts.merge(cohort_sizes, on="cohort_month", how="left")
    cohorts["retention_rate_pct"] = cohorts["active_customers"] / cohorts["cohort_size"] * 100
    cohorts["cohort_month"] = cohorts["cohort_month"].astype(str)
    return cohorts.round({"retention_rate_pct": 2}).sort_values(["cohort_month", "cohort_index"])


def _score_column(series: pd.Series, labels: list[int]) -> pd.Series:
    """Split values into up to five quantiles and map them to an R/F/M score."""
    q = min(5, series.nunique())
    if q < 2:
        return pd.Series([max(labels)] * len(series), index=series.index, dtype="int64")
    return pd.qcut(series.rank(method="first"), q, labels=labels[:q]).astype(int)


def assign_segment(score: int) -> str:
    """Assign a marketing segment from the combined RFM score."""
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
    """Aggregate customer-level RFM metrics, score and segment them."""
    today = pd.to_datetime(reference_date) if reference_date else df["sale_date"].max() + pd.Timedelta(days=1)
    rfm = (
        df.groupby("customer_id")
        .agg(
            first_purchase_date=("sale_date", "min"),
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
    rfm["customer_lifespan_days"] = (rfm["last_purchase_date"] - rfm["first_purchase_date"]).dt.days.clip(lower=0)
    rfm["avg_order_value"] = rfm["monetary_value"] / rfm["frequency"]
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
    rfm[["monetary_value", "avg_order_value"]] = rfm[["monetary_value", "avg_order_value"]].round(2)
    return rfm.sort_values(["RFM_Score", "monetary_value"], ascending=False)


def calculate_segment_summary(rfm: pd.DataFrame) -> pd.DataFrame:
    """Create a segment-level customer and revenue summary."""
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


def calculate_segment_category_profile(clean: pd.DataFrame, rfm: pd.DataFrame) -> pd.DataFrame:
    """Show strongest product categories inside each RFM segment."""
    if "category" not in clean.columns:
        return pd.DataFrame(columns=["Segment", "category", "orders", "revenue", "revenue_share_pct"])
    merged = clean.merge(rfm[["customer_id", "Segment"]], on="customer_id", how="left")
    profile = (
        merged.assign(category=merged["category"].fillna("Teadmata"))
        .groupby(["Segment", "category"])
        .agg(orders=("sale_id", "count"), revenue=("total_price", "sum"))
        .reset_index()
    )
    segment_revenue = profile.groupby("Segment")["revenue"].transform("sum")
    profile["revenue_share_pct"] = profile["revenue"] / segment_revenue * 100
    return profile.sort_values(["Segment", "revenue"], ascending=[True, False]).round(2)


def build_marketing_campaign_plan(segment_summary: pd.DataFrame) -> pd.DataFrame:
    """Create an actionable campaign plan for the RFM segments."""
    rows = [
        ("VIP Champions", "Hoida parimaid kliente", "Early access ja personaalsed VIP pakkumised", "Email + SMS", "VIP preview / tasuta tarne", "Repeat purchase rate"),
        ("Loyal", "Kasvatada ostukorvi", "Cross-sell ja komplektpakkumised", "Email", "Bundle offer", "Avg order value"),
        ("Potential", "Muuta teine ost harjumuseks", "Järgmise ostu stiimul", "Email", "-10% järgmisele ostule", "Second purchase conversion"),
        ("At Risk", "Võita klient tagasi enne kadumist", "Piiratud ajaga win-back sõnum", "Email + SMS", "Isiklik sooduskood", "Reactivation rate"),
        ("Lost", "Proovida odavat taasaktiveerimist", "Viimane tagasituleku pakkumine", "Email", "Tugevam ühekordne soodustus", "Campaign ROI"),
    ]
    plan = pd.DataFrame(rows, columns=["Segment", "goal", "message", "channel", "offer", "primary_metric"])
    if not segment_summary.empty:
        plan = plan.merge(segment_summary[["Segment", "customers", "total_revenue", "revenue_share_pct"]], on="Segment", how="left")
    return plan


def build_business_interpretation(rfm: pd.DataFrame) -> str:
    """Create a short business interpretation for Marko."""
    total_customers = int(rfm["customer_id"].nunique())
    total_revenue = rfm["monetary_value"].sum()
    vip_customers = int((rfm["Segment"] == "VIP Champions").sum())
    at_risk_customers = int((rfm["Segment"] == "At Risk").sum())
    lost_customers = int((rfm["Segment"] == "Lost").sum())
    vip_revenue = rfm.loc[rfm["Segment"] == "VIP Champions", "monetary_value"].sum()
    at_risk_revenue = rfm.loc[rfm["Segment"] == "At Risk", "monetary_value"].sum()
    vip_share = vip_revenue / total_revenue * 100 if total_revenue else 0
    at_risk_share = at_risk_revenue / total_revenue * 100 if total_revenue else 0

    return f"""# Week 8 tiimitoo API RFM raport

UrbanStyle andmestikus on {total_customers} analüüsitavat klienti, kellest {vip_customers} kuuluvad VIP Champions segmenti.
VIP kliendid annavad {vip_share:.1f}% kogukäibest.
At Risk segmendis on {at_risk_customers} klienti ja Lost segmendis {lost_customers} klienti.
At Risk segment annab veel {at_risk_share:.1f}% käibest.

## Soovitused Markole

1. VIP Champions: käivita early access programm, personaalsed pakkumised ja VIP sooduskoodid.
2. At Risk: saada win-back pakkumine enne, kui kliendid liiguvad Lost segmenti.
3. Potential ja Loyal: kasvata neid lojaalsusprogrammi ja cross-sell pakkumistega VIP segmendiks.

## Mootmise plaan

Jälgi kampaania tulemusi 30 päeva jooksul: taasostu määr, käive kliendi kohta ja keskmine ostukorv.
"""
