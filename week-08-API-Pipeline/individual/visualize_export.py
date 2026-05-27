"""Individuaalne Roll C lahendus.

Fail loob Supabase andmete põhjal nädalase tulugraafiku, KPI tabeli ja
RFM segmentide jaotuse ning ekspordib need CSV/HTML failidena.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


ROOT = Path(__file__).resolve().parent
WEEK8_DIR = ROOT.parent
OUTPUT_DIR = ROOT / "output"
SEGMENT_ORDER = ["VIP Champions", "Loyal", "Potential", "At Risk", "Lost"]
DEFAULT_ANALYSIS_DATE = "2025-02-28"


def create_weekly_chart(df_weekly: pd.DataFrame) -> go.Figure:
    """Create a Plotly line chart from weekly revenue data."""
    required_columns = {"week", "revenue"}
    missing = required_columns - set(df_weekly.columns)
    if missing:
        raise ValueError(f"Weekly chart input is missing columns: {', '.join(sorted(missing))}")

    fig = px.line(
        df_weekly,
        x="week",
        y="revenue",
        markers=True,
        title="Nädalane tulu",
        labels={"week": "Nädal", "revenue": "Tulu (EUR)"},
    )
    fig.update_traces(line={"width": 3})
    fig.update_layout(hovermode="x unified")
    return fig


def create_kpi_summary(kpis: dict[str, Any]) -> go.Figure:
    """Create a compact KPI table for Marko's weekly overview."""
    expected_keys = ["total_revenue", "orders", "unique_customers", "avg_order_value"]
    missing = [key for key in expected_keys if key not in kpis]
    if missing:
        raise ValueError(f"KPI summary is missing values: {', '.join(missing)}")

    labels = ["Kogutulu", "Tellimuste arv", "Unikaalsed kliendid", "Keskmine tellimus"]
    values = [
        f"{kpis['total_revenue']:.2f} EUR",
        kpis["orders"],
        kpis["unique_customers"],
        f"{kpis['avg_order_value']:.2f} EUR",
    ]

    fig = go.Figure(
        data=[
            go.Table(
                header={
                    "values": ["KPI", "Väärtus"],
                    "fill_color": "#d9ead3",
                    "align": "left",
                    "font": {"size": 14},
                },
                cells={
                    "values": [labels, values],
                    "align": "left",
                    "fill_color": "#f7fbf4",
                    "font": {"size": 13},
                },
            )
        ]
    )
    fig.update_layout(title="Peamised KPI-d", height=320)
    return fig


def create_segment_chart(df_segments: pd.DataFrame) -> go.Figure:
    """Create an optional RFM segment distribution chart."""
    df_segments = normalize_segment_summary(df_segments)
    required_columns = {"Segment", "customers"}
    missing = required_columns - set(df_segments.columns)
    if missing:
        raise ValueError(f"Segment chart input is missing columns: {', '.join(sorted(missing))}")

    fig = px.bar(
        df_segments.sort_values("customers", ascending=False),
        x="Segment",
        y="customers",
        text="customers",
        color="Segment",
        title="RFM segmentide jaotus",
        labels={"Segment": "Segment", "customers": "Klientide arv"},
        category_orders={"Segment": SEGMENT_ORDER},
    )
    fig.update_layout(showlegend=False)
    fig.update_traces(textposition="outside")
    return fig


def normalize_segment_summary(df_segments: pd.DataFrame) -> pd.DataFrame:
    """Accept team/individual segment summary variants and return Roll C columns."""
    segments = df_segments.copy()
    if "Segment" not in segments.columns and "segment" in segments.columns:
        segments = segments.rename(columns={"segment": "Segment"})
    if "monetary_value" not in segments.columns and "monetary" in segments.columns:
        segments = segments.rename(columns={"monetary": "monetary_value"})
    if "customers" not in segments.columns and "customer_id" in segments.columns:
        segments = (
            segments.groupby("Segment")
            .agg(customers=("customer_id", "count"), total_revenue=("monetary_value", "sum"))
            .reset_index()
        )
    all_segments = pd.DataFrame({"Segment": SEGMENT_ORDER})
    segments = all_segments.merge(segments, on="Segment", how="left")
    numeric_columns = segments.select_dtypes(include="number").columns
    segments[numeric_columns] = segments[numeric_columns].fillna(0)
    return segments


def unpack_pipeline_results(results: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, Any], pd.DataFrame | None]:
    """Read weekly, KPI and segment data from the team pipeline result dictionary."""
    if "weekly" not in results or "kpis" not in results:
        raise ValueError("Pipeline results must include 'weekly' and 'kpis'.")

    segments = results.get("segment_summary")
    if segments is None and "rfm" in results:
        segments = normalize_segment_summary(results["rfm"])

    return results["weekly"], results["kpis"], segments


def export_results(
    df_weekly: pd.DataFrame | dict[str, Any],
    kpis: dict[str, Any] | None = None,
    output_dir: str | Path = OUTPUT_DIR,
    df_segments: pd.DataFrame | None = None,
) -> dict[str, Path]:
    """Save CSV and HTML outputs with timestamped file names."""
    if isinstance(df_weekly, dict):
        df_weekly, kpis, df_segments = unpack_pipeline_results(df_weekly)
    if kpis is None:
        raise ValueError("KPI values are required unless pipeline results dict is provided.")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    paths = {
        "weekly_csv": output_path / f"weekly_aggregates_{timestamp}.csv",
        "kpis_csv": output_path / f"kpi_summary_{timestamp}.csv",
        "weekly_chart": output_path / f"weekly_revenue_{timestamp}.html",
        "kpi_chart": output_path / f"kpi_summary_{timestamp}.html",
    }

    df_weekly.to_csv(paths["weekly_csv"], index=False, encoding="utf-8")
    pd.DataFrame([kpis]).to_csv(paths["kpis_csv"], index=False, encoding="utf-8")
    create_weekly_chart(df_weekly).write_html(paths["weekly_chart"])
    create_kpi_summary(kpis).write_html(paths["kpi_chart"])

    if df_segments is not None:
        paths["segments_csv"] = output_path / f"rfm_segment_summary_{timestamp}.csv"
        paths["segment_chart"] = output_path / f"rfm_segment_chart_{timestamp}.html"
        df_segments.to_csv(paths["segments_csv"], index=False, encoding="utf-8")
        create_segment_chart(df_segments).write_html(paths["segment_chart"])

    return paths


def load_week8_pipeline_module() -> Any:
    """Lae peamine Week 8 pipeline moodulina, kuigi kaustanimes on sidekriips."""
    module_path = WEEK8_DIR / "week8_api_pipeline.py"
    spec = importlib.util.spec_from_file_location("week8_api_pipeline", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Ei saa laadida pipeline moodulit: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def build_results_from_supabase(analysis_date: str | None = DEFAULT_ANALYSIS_DATE) -> dict[str, Any]:
    """Lae Supabase andmed ja teisenda need Roll C ekspordi sisendkujule."""
    pipeline = load_week8_pipeline_module()
    supabase = pipeline.get_supabase_client()
    if supabase is None:
        raise RuntimeError("Supabase seadistus puudub. Lisa SUPABASE_URL ja SUPABASE_ANON_KEY.")

    sales = pipeline.fetch_table(supabase, "sales", date_column="sale_date", end_date=analysis_date)
    customers = pipeline.fetch_table(supabase, "customers")
    if sales.empty or customers.empty:
        raise RuntimeError("Supabase API ei tagastanud sales/customers andmeid.")

    clean_orders = pipeline.normalize_orders(sales, customers, analysis_date=analysis_date)
    rfm = pipeline.calculate_rfm(clean_orders, reference_date=analysis_date)

    weekly = (
        clean_orders.resample("W-MON", on="sale_date", label="left", closed="left")
        .agg(
            revenue=("total_price", "sum"),
            orders=("total_price", "count"),
            unique_customers=("customer_id", "nunique"),
        )
        .reset_index()
        .rename(columns={"sale_date": "week"})
    )
    weekly["avg_order_value"] = weekly["revenue"] / weekly["orders"]
    weekly[["revenue", "avg_order_value"]] = weekly[["revenue", "avg_order_value"]].round(2)

    total_revenue = float(clean_orders["total_price"].sum())
    orders = len(clean_orders)
    kpis = {
        "total_revenue": round(total_revenue, 2),
        "orders": int(orders),
        "unique_customers": int(clean_orders["customer_id"].nunique()),
        "avg_order_value": round(total_revenue / orders, 2) if orders else 0.0,
    }

    segment_summary = normalize_segment_summary(rfm)
    return {"weekly": weekly, "kpis": kpis, "segment_summary": segment_summary, "rfm": rfm}


def main() -> None:
    """Käivita Roll C iseseisev test ja kirjuta väljundfailide asukohad."""
    parser = argparse.ArgumentParser(description="Week 8 individual Roll C export Supabase andmetest")
    parser.add_argument(
        "--date",
        default=DEFAULT_ANALYSIS_DATE,
        help="Valikuline analüüsi lõppkuupäev formaadis YYYY-MM-DD.",
    )
    args = parser.parse_args()

    results = build_results_from_supabase(analysis_date=args.date)
    paths = export_results(results)

    print("Roll C väljundfailid loodud:")
    print(f"RFM segmentide arv: {results['segment_summary']['Segment'].nunique()}")
    for name, path in paths.items():
        print(f"- {name}: {path}")


if __name__ == "__main__":
    main()
