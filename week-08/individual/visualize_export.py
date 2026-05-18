"""Individuaalne Roll C lahendus.

Fail loob näidisandmete põhjal nädalase tulugraafiku, KPI tabeli ja
RFM segmentide jaotuse ning ekspordib need CSV/HTML failidena.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"


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
    )
    fig.update_layout(showlegend=False)
    fig.update_traces(textposition="outside")
    return fig


def export_results(
    df_weekly: pd.DataFrame,
    kpis: dict[str, Any],
    output_dir: str | Path = OUTPUT_DIR,
    df_segments: pd.DataFrame | None = None,
) -> dict[str, Path]:
    """Save CSV and HTML outputs with timestamped file names."""
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


def sample_weekly_data() -> pd.DataFrame:
    """Small local dataset for testing Role C without the API modules."""
    weekly = pd.DataFrame(
        {
            "week": pd.to_datetime(["2025-01-06", "2025-01-13", "2025-01-20", "2025-01-27"]),
            "revenue": [1840.50, 2135.20, 1988.00, 2460.75],
            "orders": [18, 22, 20, 25],
            "unique_customers": [14, 17, 16, 20],
        }
    )
    weekly["avg_order_value"] = (weekly["revenue"] / weekly["orders"]).round(2)
    return weekly


def sample_kpis(df_weekly: pd.DataFrame) -> dict[str, Any]:
    """Arvuta näidisnädalate põhjal KPI väärtused."""
    orders = int(df_weekly["orders"].sum())
    revenue = float(df_weekly["revenue"].sum())
    return {
        "total_revenue": round(revenue, 2),
        "orders": orders,
        "unique_customers": int(df_weekly["unique_customers"].max()),
        "avg_order_value": round(revenue / orders, 2) if orders else 0,
    }


def sample_segments() -> pd.DataFrame:
    """Loo väike näidis RFM segmentide tabel graafiku testimiseks."""
    return pd.DataFrame(
        {
            "Segment": ["VIP Champions", "Loyal", "Potential", "At Risk"],
            "customers": [42, 88, 124, 36],
            "total_revenue": [41500, 52200, 38400, 9100],
        }
    )


def main() -> None:
    """Käivita Roll C iseseisev test ja kirjuta väljundfailide asukohad."""
    weekly = sample_weekly_data()
    kpis = sample_kpis(weekly)
    segments = sample_segments()
    paths = export_results(weekly, kpis, df_segments=segments)

    print("Roll C väljundfailid loodud:")
    for name, path in paths.items():
        print(f"- {name}: {path}")


if __name__ == "__main__":
    main()
