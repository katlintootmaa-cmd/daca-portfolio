from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


TEAM_DIR = Path(__file__).resolve().parents[1]
if str(TEAM_DIR) not in sys.path:
    sys.path.insert(0, str(TEAM_DIR))

from transform import (  # noqa: E402
    assign_segment,
    build_marketing_campaign_plan,
    calculate_cohort_retention,
    calculate_data_quality_report,
    calculate_rfm,
    calculate_segment_summary,
)


def sample_clean_sales() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "sale_id": [1, 2, 3, 4, 5],
            "customer_id": [101, 101, 102, 103, 103],
            "sale_date": pd.to_datetime(["2025-01-01", "2025-02-01", "2025-01-15", "2025-01-20", "2025-03-01"]),
            "total_price": [100.0, 150.0, 80.0, 40.0, 70.0],
            "first_name": ["A", "A", "B", "C", "C"],
            "last_name": ["One", "One", "Two", "Three", "Three"],
            "email": ["a@example.com", "a@example.com", None, "c@example.com", "c@example.com"],
            "phone": [None, None, "+3721", None, None],
            "has_email": [True, True, False, True, True],
            "has_phone": [False, False, True, False, False],
            "has_contact": [True, True, True, True, True],
            "city": ["Tallinn", "Tallinn", "Tartu", "Parnu", "Parnu"],
            "loyalty_tier": ["gold", "gold", "silver", None, None],
        }
    )


def test_assign_segment_boundaries() -> None:
    assert assign_segment(15) == "VIP Champions"
    assert assign_segment(10) == "Loyal"
    assert assign_segment(7) == "Potential"
    assert assign_segment(4) == "At Risk"
    assert assign_segment(3) == "Lost"


def test_rfm_summary_matches_revenue() -> None:
    sales = sample_clean_sales()
    rfm = calculate_rfm(sales, reference_date="2025-03-31")
    summary = calculate_segment_summary(rfm)

    assert "first_purchase_date" in rfm.columns
    assert round(rfm["monetary_value"].sum(), 2) == round(sales["total_price"].sum(), 2)
    assert round(summary["total_revenue"].sum(), 2) == round(sales["total_price"].sum(), 2)


def test_data_quality_report_counts_basic_issues() -> None:
    raw = pd.DataFrame(
        {
            "customer_id": [1, None, 2, 2],
            "sale_date": ["2025-01-01", "bad-date", "2025-01-02", "2025-01-02"],
            "total_price": [10, 20, -1, -1],
        }
    )
    clean = sample_clean_sales()
    quality = calculate_data_quality_report(raw, clean)

    metrics = dict(zip(quality["metric"], quality["value"], strict=True))
    assert metrics["missing_customer_id"] == 1
    assert metrics["invalid_sale_date"] == 1
    assert metrics["non_positive_revenue"] == 2


def test_cohort_retention_and_campaign_plan_are_actionable() -> None:
    sales = sample_clean_sales()
    rfm = calculate_rfm(sales, reference_date="2025-03-31")
    segment_summary = calculate_segment_summary(rfm)
    cohort = calculate_cohort_retention(sales)
    campaign_plan = build_marketing_campaign_plan(segment_summary)

    assert {"cohort_month", "cohort_index", "retention_rate_pct"}.issubset(cohort.columns)
    assert set(campaign_plan["Segment"]) == {"VIP Champions", "Loyal", "Potential", "At Risk", "Lost"}
    assert "primary_metric" in campaign_plan.columns
