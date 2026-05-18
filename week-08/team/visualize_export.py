"""Roll C: Visualization + Saving.

See moodul loob töödeldud andmetest Plotly graafikud ja salvestab
tulemused CSV, HTML ja Markdown failidena output kausta.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


logger = logging.getLogger(__name__)
SEGMENT_ORDER = ["VIP Champions", "Loyal", "Potential", "At Risk", "Lost"]


def create_weekly_chart(df_weekly: pd.DataFrame) -> go.Figure:
    """Loo nädalase tulu joondiagramm."""
    return px.line(
        df_weekly,
        x="week",
        y="revenue",
        markers=True,
        title="Nädalane tulu",
        labels={"week": "Nädal", "revenue": "Tulu (EUR)"},
    )


def create_kpi_summary(kpis: dict[str, Any]) -> go.Figure:
    """Loo KPI tabel total revenue, orders, customers ja avg order väärtustega."""
    return go.Figure(
        data=[
            go.Table(
                header={"values": ["KPI", "Väärtus"], "fill_color": "#d9ead3", "align": "left"},
                cells={
                    "values": [
                        ["Total revenue", "Orders", "Unique customers", "Avg order value"],
                        [
                            f"{kpis['total_revenue']:.2f} EUR",
                            kpis["orders"],
                            kpis["unique_customers"],
                            f"{kpis['avg_order_value']:.2f} EUR",
                        ],
                    ],
                    "align": "left",
                },
            )
        ]
    )


def create_segment_chart(segment_summary: pd.DataFrame) -> go.Figure:
    """Loo tulpdiagramm RFM segmentide klientide arvust."""
    fig = px.bar(
        segment_summary.sort_values("customers", ascending=False),
        x="Segment",
        y="customers",
        text="customers",
        title="UrbanStyle kliendisegmentide jaotus",
        labels={"Segment": "Segment", "customers": "Klientide arv"},
        color="Segment",
        category_orders={"Segment": SEGMENT_ORDER},
    )
    fig.update_layout(showlegend=False)
    return fig


def create_rfm_scatter(rfm: pd.DataFrame) -> go.Figure:
    """Loo RFM hajuvusdiagramm recency, monetary ja frequency näitajatega."""
    return px.scatter(
        rfm,
        x="recency_days",
        y="monetary_value",
        color="Segment",
        size="frequency",
        hover_data=["customer_name", "email", "frequency", "RFM_Score"],
        title="UrbanStyle kliendisegmendid RFM analüüsi põhjal",
        labels={
            "recency_days": "Päevi viimasest ostust",
            "monetary_value": "Kogukulutus (EUR)",
            "frequency": "Ostude arv",
        },
        category_orders={"Segment": SEGMENT_ORDER},
    )


def create_top_vip_chart(rfm: pd.DataFrame) -> go.Figure:
    """Loo top 10 VIP kliendi tulpdiagramm kogukulutuse järgi."""
    top_vip = rfm[rfm["Segment"] == "VIP Champions"].nlargest(10, "monetary_value").copy()
    if top_vip.empty:
        top_vip = rfm.nlargest(10, "monetary_value").copy()
    fig = px.bar(
        top_vip.sort_values("monetary_value"),
        x="monetary_value",
        y="customer_name",
        orientation="h",
        text="monetary_value",
        title="Top 10 VIP klienti kogukulutuse järgi",
        labels={"monetary_value": "Kogukulutus (EUR)", "customer_name": "Klient"},
    )
    fig.update_traces(texttemplate="%{text:.0f} EUR", textposition="outside")
    return fig


def export_results(results: dict[str, Any], output_dir: str | Path = "output") -> dict[str, Path]:
    """Salvesta kõik raportid ja graafikud ajatempliga failinimedega."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    paths = {
        "weekly_csv": output_path / f"weekly_aggregates_{date_str}.csv",
        "kpis_csv": output_path / f"kpis_{date_str}.csv",
        "rfm_csv": output_path / f"rfm_segments_{date_str}.csv",
        "segment_summary_csv": output_path / f"rfm_segment_summary_{date_str}.csv",
        "report_md": output_path / f"rfm_business_report_{date_str}.md",
        "weekly_chart": output_path / f"weekly_revenue_{date_str}.html",
        "kpi_chart": output_path / f"kpi_summary_{date_str}.html",
        "segment_chart": output_path / f"rfm_segmentide_jaotus_{date_str}.html",
        "rfm_scatter": output_path / f"rfm_segmentide_scatter_{date_str}.html",
        "top_vip_chart": output_path / f"rfm_top_10_vip_{date_str}.html",
    }

    results["weekly"].to_csv(paths["weekly_csv"], index=False, encoding="utf-8")
    pd.DataFrame([results["kpis"]]).to_csv(paths["kpis_csv"], index=False, encoding="utf-8")
    results["rfm"].to_csv(paths["rfm_csv"], index=False, encoding="utf-8")
    results["segment_summary"].to_csv(paths["segment_summary_csv"], index=False, encoding="utf-8")
    paths["report_md"].write_text(results["business_interpretation"], encoding="utf-8")

    create_weekly_chart(results["weekly"]).write_html(paths["weekly_chart"])
    create_kpi_summary(results["kpis"]).write_html(paths["kpi_chart"])
    create_segment_chart(results["segment_summary"]).write_html(paths["segment_chart"])
    create_rfm_scatter(results["rfm"]).write_html(paths["rfm_scatter"])
    create_top_vip_chart(results["rfm"]).write_html(paths["top_vip_chart"])

    logger.info("Väljundfailid salvestatud kausta %s", output_path)
    return paths
