"""Roll C: visualization and export for the Week 8 marketing pipeline."""

from __future__ import annotations

import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


logger = logging.getLogger(__name__)
SEGMENT_ORDER = ["VIP Champions", "Loyal", "Potential", "At Risk", "Lost"]


def create_weekly_chart(df_weekly: pd.DataFrame) -> go.Figure:
    """Create a weekly revenue line chart."""
    fig = px.line(
        df_weekly,
        x="week",
        y="revenue",
        markers=True,
        title="Nadalane tulu",
        labels={"week": "Nadal", "revenue": "Tulu (EUR)"},
        custom_data=["week_label", "orders", "unique_customers"],
    )
    fig.update_traces(
        hovertemplate=(
            "Nadal=%{customdata[0]}<br>"
            "Tulu (EUR)=%{y:.2f}<br>"
            "Tellimusi=%{customdata[1]}<br>"
            "Unikaalseid kliente=%{customdata[2]}<extra></extra>"
        )
    )
    return fig


def create_monthly_chart(df_monthly: pd.DataFrame) -> go.Figure:
    """Create a monthly revenue line chart."""
    return px.line(
        df_monthly,
        x="month",
        y="revenue",
        markers=True,
        title="Kuukäive",
        labels={"month": "Kuu", "revenue": "Tulu (EUR)"},
    )


def create_city_chart(df_city: pd.DataFrame) -> go.Figure:
    """Create a city revenue bar chart."""
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


def create_channel_chart(df_channel: pd.DataFrame) -> go.Figure:
    """Create a revenue by channel bar chart."""
    if df_channel.empty:
        return create_empty_figure("Kanaliandmed puuduvad")
    fig = px.bar(
        df_channel,
        x="channel",
        y="revenue",
        text="revenue",
        title="Tulu kanali kaupa",
        labels={"channel": "Kanal", "revenue": "Tulu (EUR)"},
    )
    fig.update_traces(texttemplate="%{text:.0f} EUR", textposition="outside")
    return fig


def create_kpi_summary(kpis: dict[str, Any]) -> go.Figure:
    """Create a KPI table."""
    labels = ["Total revenue", "Orders", "Unique customers", "Avg order value", "Revenue per customer"]
    values = [
        f"{kpis['total_revenue']:.2f} EUR",
        kpis["orders"],
        kpis["unique_customers"],
        f"{kpis['avg_order_value']:.2f} EUR",
        f"{kpis.get('revenue_per_customer', 0):.2f} EUR",
    ]
    return go.Figure(
        data=[
            go.Table(
                header={"values": ["KPI", "Vaartus"], "fill_color": "#d9ead3", "align": "left"},
                cells={"values": [labels, values], "align": "left"},
            )
        ]
    )


def create_data_quality_table(data_quality: pd.DataFrame) -> go.Figure:
    """Create a data quality table."""
    return go.Figure(
        data=[
            go.Table(
                header={"values": ["Metric", "Value", "Description"], "fill_color": "#e5e7eb", "align": "left"},
                cells={
                    "values": [data_quality["metric"], data_quality["value"], data_quality["description"]],
                    "align": "left",
                },
            )
        ]
    )


def create_campaign_plan_table(campaign_plan: pd.DataFrame) -> go.Figure:
    """Create a campaign plan table."""
    columns = ["Segment", "goal", "message", "channel", "offer", "primary_metric"]
    headers = ["Segment", "Eesmärk", "Sõnum", "Kanal", "Pakkumine", "Peamine mõõdik"]
    return go.Figure(
        data=[
            go.Table(
                header={"values": headers, "fill_color": "#dbeafe", "align": "left"},
                cells={"values": [campaign_plan[column] for column in columns], "align": "left"},
            )
        ]
    )


def create_segment_chart(segment_summary: pd.DataFrame) -> go.Figure:
    """Create an RFM segment distribution chart."""
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
    """Create an RFM scatter plot without exposing direct contact data."""
    return px.scatter(
        rfm,
        x="recency_days",
        y="monetary_value",
        color="Segment",
        size="frequency",
        hover_data=["customer_name", "city", "frequency", "RFM_Score"],
        title="UrbanStyle kliendisegmendid RFM analüüsi põhjal",
        labels={
            "recency_days": "Paevi viimasest ostust",
            "monetary_value": "Kogukulutus (EUR)",
            "frequency": "Ostude arv",
        },
        category_orders={"Segment": SEGMENT_ORDER},
    )


def create_top_vip_chart(rfm: pd.DataFrame) -> go.Figure:
    """Create a top VIP customers chart by spending."""
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


def create_cohort_chart(cohort_retention: pd.DataFrame) -> go.Figure:
    """Create a cohort retention heatmap."""
    if cohort_retention.empty:
        return create_empty_figure("Cohort retention puudub")
    matrix = cohort_retention.pivot(index="cohort_month", columns="cohort_index", values="retention_rate_pct").fillna(0)
    return px.imshow(
        matrix,
        aspect="auto",
        text_auto=".0f",
        color_continuous_scale="YlGnBu",
        title="Cohort retention esimese ostukuu põhjal (%)",
        labels={"x": "Kuud esimesest ostust", "y": "Esimese ostu kuu", "color": "Retention %"},
    )


def create_category_profile_chart(segment_category_profile: pd.DataFrame) -> go.Figure:
    """Create a category profile chart by segment."""
    if segment_category_profile.empty:
        return create_empty_figure("Tootekategooria profiil puudub")
    top_profile = segment_category_profile.groupby("Segment", group_keys=False).head(3)
    return px.bar(
        top_profile,
        x="Segment",
        y="revenue",
        color="category",
        title="Top kategooriad RFM segmentide loikes",
        labels={"revenue": "Tulu (EUR)", "category": "Kategooria"},
        category_orders={"Segment": SEGMENT_ORDER},
    )


def create_empty_figure(title: str) -> go.Figure:
    """Return a small placeholder figure for optional missing reports."""
    fig = go.Figure()
    fig.update_layout(title=title, xaxis={"visible": False}, yaxis={"visible": False})
    return fig


def _html_table(df: pd.DataFrame, max_rows: int = 8, headers: dict[str, str] | None = None) -> str:
    """Render a compact dataframe as HTML."""
    if df.empty:
        return "<p>Andmed puuduvad.</p>"
    table = df.head(max_rows).rename(columns=headers or {})
    return table.to_html(index=False, classes="mini-table", border=0)


def _executive_summary(results: dict[str, Any]) -> str:
    """Build the dashboard's executive summary cards."""
    kpis = results["kpis"]
    segment_summary = results["segment_summary"]
    vip = segment_summary[segment_summary["Segment"] == "VIP Champions"]
    at_risk = segment_summary[segment_summary["Segment"] == "At Risk"]
    vip_text = "puudub"
    at_risk_text = "puudub"
    if not vip.empty:
        row = vip.iloc[0]
        vip_text = f"{int(row['customers'])} klienti, {row['revenue_share_pct']:.1f}% käibest"
    if not at_risk.empty:
        row = at_risk.iloc[0]
        at_risk_text = f"{int(row['customers'])} klienti, {row['revenue_share_pct']:.1f}% käibest"
    source = results.get("data_source", "unknown")
    source_note = ""
    if source != "supabase_api":
        source_note = f'<p class="warning">Hoiatus: raport kasutab andmeallikat "{source}", mitte live Supabase API tulemust.</p>'
    revenue_millions = kpis["total_revenue"] / 1_000_000
    return f"""
    <section class="summary">
      <div><span>Kogukäive</span><strong>{revenue_millions:.1f} mln EUR</strong></div>
      <div><span>Tellimused</span><strong>{kpis['orders']}</strong></div>
      <div><span>VIP Champions</span><strong>{vip_text}</strong></div>
      <div><span>At Risk</span><strong>{at_risk_text}</strong></div>
    </section>
    {source_note}
    <section class="insight">
      <h2>Otsus Markole</h2>
      <p>Hoia VIP kliente lojaalsusprogrammiga, tee At Risk segmendile win-back kampaania ning kasuta Loyal ja Potential segmentides cross-selli.</p>
    </section>
    """


def write_combined_dashboard(results: dict[str, Any], path: Path) -> None:
    """Save all team figures into one HTML dashboard."""
    figures = [
        create_kpi_summary(results["kpis"]),
        create_weekly_chart(results["weekly"]),
        create_monthly_chart(results["monthly"]),
        create_segment_chart(results["segment_summary"]),
        create_rfm_scatter(results["rfm"]),
        create_top_vip_chart(results["rfm"]),
    ]
    sections = [
        f'<section class="chart">{figure.to_html(full_html=False, include_plotlyjs="cdn" if index == 0 else False)}</section>'
        for index, figure in enumerate(figures)
    ]
    html = f"""<!doctype html>
<html lang="et">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Week 8 tiimitoo koondvisuaalid</title>
  <style>
    body {{
      margin: 0;
      background: #f5f7fb;
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
    h2 {{
      margin: 0 0 8px;
      font-size: 18px;
    }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 12px;
    }}
    .summary div,
    .insight,
    .chart {{
      background: #ffffff;
      border: 1px solid #d9e2ec;
      border-radius: 8px;
      padding: 14px;
      overflow: hidden;
    }}
    .summary span {{
      display: block;
      color: #64748b;
      font-size: 13px;
    }}
    .summary strong {{
      display: block;
      margin-top: 6px;
      font-size: 20px;
    }}
    .warning {{
      background: #fff7ed;
      border: 1px solid #fed7aa;
      border-radius: 8px;
      margin: 0;
      padding: 12px 14px;
    }}
    .mini-table {{
      width: 100%;
      border-collapse: collapse;
      background: #ffffff;
      font-size: 13px;
    }}
    .mini-table th,
    .mini-table td {{
      border-bottom: 1px solid #e5e7eb;
      padding: 8px;
      text-align: left;
    }}
    main > section.chart:nth-of-type(3),
    main > section.chart:nth-of-type(4) {{
      display: none;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Week 8 tiimitoo koondvisuaalid</h1>
  </header>
  <main>
    {_executive_summary(results)}
    <section class="chart">
      <h2>Kampaaniaplaan</h2>
      {_html_table(
        results["campaign_plan"],
        max_rows=10,
        headers={
          "Segment": "Segment",
          "goal": "Eesmärk",
          "message": "Sõnum",
          "channel": "Kanal",
          "offer": "Pakkumine",
          "primary_metric": "Peamine mõõdik",
          "customers": "Kliente",
          "total_revenue": "Kogukäive",
          "revenue_share_pct": "Käibe osakaal %",
        },
      )}
    </section>
    {"".join(sections)}
  </main>
</body>
</html>
"""
    path.write_text(html, encoding="utf-8")


def _write_latest_copies(paths: dict[str, Path], output_path: Path) -> None:
    """Copy timestamped outputs to stable *_latest filenames."""
    latest_names = {
        "weekly_chart": "weekly_revenue_latest.html",
        "monthly_chart": "monthly_revenue_latest.html",
        "city_chart": "city_revenue_latest.html",
        "channel_chart": "channel_revenue_latest.html",
        "kpi_chart": "kpi_summary_latest.html",
        "segment_chart": "rfm_segmentide_jaotus_latest.html",
        "rfm_scatter": "rfm_segmentide_scatter_latest.html",
        "top_vip_chart": "rfm_top_10_vip_latest.html",
        "cohort_chart": "cohort_retention_latest.html",
        "category_profile_chart": "segment_category_profile_latest.html",
        "campaign_plan_chart": "marketing_campaign_plan_latest.html",
        "combined_dashboard": "team_dashboard_latest.html",
    }
    for key, latest_name in latest_names.items():
        source = paths.get(key)
        if source and source.exists():
            latest_path = output_path / latest_name
            shutil.copyfile(source, latest_path)
            paths[f"{key}_latest"] = latest_path


def export_results(results: dict[str, Any], output_dir: str | Path = "output") -> dict[str, Path]:
    """Save visual HTML reports with timestamped names and latest aliases."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    paths = {
        "weekly_chart": output_path / f"weekly_revenue_{date_str}.html",
        "monthly_chart": output_path / f"monthly_revenue_{date_str}.html",
        "city_chart": output_path / f"city_revenue_{date_str}.html",
        "channel_chart": output_path / f"channel_revenue_{date_str}.html",
        "kpi_chart": output_path / f"kpi_summary_{date_str}.html",
        "segment_chart": output_path / f"rfm_segmentide_jaotus_{date_str}.html",
        "rfm_scatter": output_path / f"rfm_segmentide_scatter_{date_str}.html",
        "top_vip_chart": output_path / f"rfm_top_10_vip_{date_str}.html",
        "cohort_chart": output_path / f"cohort_retention_{date_str}.html",
        "category_profile_chart": output_path / f"segment_category_profile_{date_str}.html",
        "campaign_plan_chart": output_path / f"marketing_campaign_plan_{date_str}.html",
        "combined_dashboard": output_path / f"team_dashboard_{date_str}.html",
    }

    html_options = {"include_plotlyjs": "cdn", "full_html": True}
    create_weekly_chart(results["weekly"]).write_html(paths["weekly_chart"], **html_options)
    create_monthly_chart(results["monthly"]).write_html(paths["monthly_chart"], **html_options)
    create_city_chart(results["city"]).write_html(paths["city_chart"], **html_options)
    create_channel_chart(results["channel"]).write_html(paths["channel_chart"], **html_options)
    create_kpi_summary(results["kpis"]).write_html(paths["kpi_chart"], **html_options)
    create_segment_chart(results["segment_summary"]).write_html(paths["segment_chart"], **html_options)
    create_rfm_scatter(results["rfm"]).write_html(paths["rfm_scatter"], **html_options)
    create_top_vip_chart(results["rfm"]).write_html(paths["top_vip_chart"], **html_options)
    create_cohort_chart(results["cohort_retention"]).write_html(paths["cohort_chart"], **html_options)
    create_category_profile_chart(results["segment_category_profile"]).write_html(paths["category_profile_chart"], **html_options)
    create_campaign_plan_table(results["campaign_plan"]).write_html(paths["campaign_plan_chart"], **html_options)
    write_combined_dashboard(results, paths["combined_dashboard"])
    _write_latest_copies(paths, output_path)

    logger.info("Väljundfailid salvestatud kausta %s", output_path)
    return paths
