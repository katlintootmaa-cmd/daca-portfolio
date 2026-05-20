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
    fig = px.line(
        df_weekly,
        x="week",
        y="revenue",
        markers=True,
        title="Nädalane tulu",
        labels={"week": "Nädal", "revenue": "Tulu (EUR)"},
        custom_data=["week_label", "orders", "unique_customers"],
    )
    fig.update_traces(
        hovertemplate=(
            "Nädal=%{customdata[0]}<br>"
            "Tulu (EUR)=%{y:.2f}<br>"
            "Tellimusi=%{customdata[1]}<br>"
            "Unikaalseid kliente=%{customdata[2]}<extra></extra>"
        )
    )
    return fig


def create_monthly_chart(df_monthly: pd.DataFrame) -> go.Figure:
    """Loo kuukäibe joondiagramm."""
    return px.line(
        df_monthly,
        x="month",
        y="revenue",
        markers=True,
        title="Kuukäive",
        labels={"month": "Kuu", "revenue": "Tulu (EUR)"},
    )


def create_city_chart(df_city: pd.DataFrame) -> go.Figure:
    """Loo linnade kogutulu tulpdiagramm."""
    fig = px.bar(
        df_city.sort_values("revenue"),
        x="revenue",
        y="city",
        orientation="h",
        text="revenue",
        title="Tulu linnade kaupa",
        labels={"city": "Linn", "revenue": "Tulu (EUR)"},
    )
    fig.update_traces(texttemplate="%{text:.0f} EUR", textposition="outside")
    return fig


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


def write_combined_dashboard(results: dict[str, Any], path: Path) -> None:
    """Salvesta tiimitöö graafikud ühte HTML faili."""
    figures = [
        create_kpi_summary(results["kpis"]),
        create_weekly_chart(results["weekly"]),
        create_monthly_chart(results["monthly"]),
        create_city_chart(results["city"]),
        create_segment_chart(results["segment_summary"]),
        create_rfm_scatter(results["rfm"]),
        create_top_vip_chart(results["rfm"]),
    ]
    sections = [
        f'<section class="chart">{figure.to_html(full_html=False, include_plotlyjs=index == 0)}</section>'
        for index, figure in enumerate(figures)
    ]
    html = f"""<!doctype html>
<html lang="et">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Week 8 tiimitöö koondvisuaalid</title>
  <style>
    body {{
      margin: 0;
      background: #f4f6f9;
      color: #1f2937;
      font-family: Arial, sans-serif;
    }}
    header {{
      padding: 28px 32px 12px;
      background: #ffffff;
      border-bottom: 1px solid #d9e2ec;
    }}
    main {{
      display: grid;
      gap: 18px;
      padding: 22px 32px 36px;
    }}
    h1 {{
      margin: 0;
      font-size: 30px;
    }}
    .chart {{
      background: #ffffff;
      border: 1px solid #d9e2ec;
      border-radius: 8px;
      padding: 12px;
      overflow: hidden;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Week 8 tiimitöö koondvisuaalid</h1>
  </header>
  <main>
    {"".join(sections)}
  </main>
</body>
</html>
"""
    path.write_text(html, encoding="utf-8")


def export_results(results: dict[str, Any], output_dir: str | Path = "output") -> dict[str, Path]:
    """Salvesta kõik raportid ja graafikud ajatempliga failinimedega."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    paths = {
        "weekly_csv": output_path / f"weekly_aggregates_{date_str}.csv",
        "monthly_csv": output_path / f"monthly_report_{date_str}.csv",
        "city_csv": output_path / f"city_report_{date_str}.csv",
        "kpis_csv": output_path / f"kpis_{date_str}.csv",
        "rfm_csv": output_path / f"rfm_segments_{date_str}.csv",
        "segment_summary_csv": output_path / f"rfm_segment_summary_{date_str}.csv",
        "report_md": output_path / f"rfm_business_report_{date_str}.md",
        "weekly_chart": output_path / f"weekly_revenue_{date_str}.html",
        "monthly_chart": output_path / f"monthly_revenue_{date_str}.html",
        "city_chart": output_path / f"city_revenue_{date_str}.html",
        "kpi_chart": output_path / f"kpi_summary_{date_str}.html",
        "segment_chart": output_path / f"rfm_segmentide_jaotus_{date_str}.html",
        "rfm_scatter": output_path / f"rfm_segmentide_scatter_{date_str}.html",
        "top_vip_chart": output_path / f"rfm_top_10_vip_{date_str}.html",
        "combined_dashboard": output_path / f"team_dashboard_{date_str}.html",
    }

    results["weekly"].to_csv(paths["weekly_csv"], index=False, encoding="utf-8")
    results["monthly"].to_csv(paths["monthly_csv"], index=False, encoding="utf-8")
    results["city"].to_csv(paths["city_csv"], index=False, encoding="utf-8")
    pd.DataFrame([results["kpis"]]).to_csv(paths["kpis_csv"], index=False, encoding="utf-8")
    results["rfm"].to_csv(paths["rfm_csv"], index=False, encoding="utf-8")
    results["segment_summary"].to_csv(paths["segment_summary_csv"], index=False, encoding="utf-8")
    paths["report_md"].write_text(results["business_interpretation"], encoding="utf-8")

    create_weekly_chart(results["weekly"]).write_html(paths["weekly_chart"])
    create_monthly_chart(results["monthly"]).write_html(paths["monthly_chart"])
    create_city_chart(results["city"]).write_html(paths["city_chart"])
    create_kpi_summary(results["kpis"]).write_html(paths["kpi_chart"])
    create_segment_chart(results["segment_summary"]).write_html(paths["segment_chart"])
    create_rfm_scatter(results["rfm"]).write_html(paths["rfm_scatter"])
    create_top_vip_chart(results["rfm"]).write_html(paths["top_vip_chart"])
    write_combined_dashboard(results, paths["combined_dashboard"])

    logger.info("Väljundfailid salvestatud kausta %s", output_path)
    return paths
