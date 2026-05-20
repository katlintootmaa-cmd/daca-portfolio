"""Build one Week 8 HTML page from team, individual and pipeline outputs."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


ROOT = Path(__file__).resolve().parent
WEEK_ROOT = ROOT.parent
TEAM_OUTPUT = WEEK_ROOT / "team" / "output"
INDIVIDUAL_OUTPUT = ROOT / "output"
PIPELINE_OUTPUT = INDIVIDUAL_OUTPUT
COMBINED_OUTPUT = ROOT / "combined_visuals.html"
SEGMENT_ORDER = ["VIP Champions", "Loyal", "Potential", "At Risk", "Lost"]


def latest_file(folder: Path, pattern: str) -> Path | None:
    """Return the newest matching output file."""
    files = sorted(folder.glob(pattern), key=lambda path: path.stat().st_mtime, reverse=True)
    return files[0] if files else None


def read_latest(folder: Path, pattern: str) -> pd.DataFrame | None:
    """Read the newest CSV for a report type, if it exists."""
    path = latest_file(folder, pattern)
    if path is None:
        return None
    return pd.read_csv(path)


def format_eur(value: float) -> str:
    """Format a number as an EUR value."""
    return f"{value:,.2f} EUR".replace(",", " ")


def kpi_table(kpis: pd.DataFrame, title: str) -> go.Figure:
    """Create a compact KPI table from a one-row CSV."""
    row = kpis.iloc[0].to_dict()
    labels = ["Kogutulu", "Tellimused", "Unikaalsed kliendid", "Keskmine tellimus"]
    values = [
        format_eur(float(row.get("total_revenue", 0))),
        int(row.get("orders", 0)),
        int(row.get("unique_customers", 0)),
        format_eur(float(row.get("avg_order_value", 0))),
    ]
    fig = go.Figure(
        data=[
            go.Table(
                header={"values": ["KPI", "Väärtus"], "fill_color": "#e8eef8", "align": "left"},
                cells={"values": [labels, values], "fill_color": "#f8fafc", "align": "left"},
            )
        ]
    )
    fig.update_layout(title=title, height=280, margin={"t": 55, "b": 15, "l": 15, "r": 15})
    return fig


def weekly_chart(weekly: pd.DataFrame, title: str) -> go.Figure:
    """Create weekly revenue chart."""
    fig = px.line(
        weekly,
        x="week",
        y="revenue",
        markers=True,
        title=title,
        labels={"week": "Nädal", "revenue": "Tulu (EUR)"},
    )
    fig.update_traces(line={"width": 3})
    fig.update_layout(hovermode="x unified")
    return fig


def segment_chart(segments: pd.DataFrame, title: str) -> go.Figure:
    """Create RFM segment distribution chart."""
    fig = px.bar(
        segments.sort_values("customers", ascending=False),
        x="Segment",
        y="customers",
        color="Segment",
        text="customers",
        title=title,
        labels={"Segment": "Segment", "customers": "Klientide arv"},
        category_orders={"Segment": SEGMENT_ORDER},
    )
    fig.update_layout(showlegend=False)
    fig.update_traces(textposition="outside")
    return fig


def top_customers_chart(rfm: pd.DataFrame, title: str) -> go.Figure:
    """Create a top-customer chart from an RFM report."""
    monetary_column = "monetary_value" if "monetary_value" in rfm.columns else "monetary"
    name_column = "customer_name" if "customer_name" in rfm.columns else "customer_id"
    top = rfm.nlargest(10, monetary_column).sort_values(monetary_column)
    fig = px.bar(
        top,
        x=monetary_column,
        y=name_column,
        orientation="h",
        text=monetary_column,
        title=title,
        labels={monetary_column: "Kogukulutus (EUR)", name_column: "Klient"},
    )
    fig.update_traces(texttemplate="%{text:.0f} EUR", textposition="outside")
    fig.update_layout(margin={"l": 120, "r": 35, "t": 60, "b": 45})
    return fig


def rfm_scatter(rfm: pd.DataFrame, title: str) -> go.Figure:
    """Create an RFM scatter plot from the main pipeline report."""
    monetary_column = "monetary_value" if "monetary_value" in rfm.columns else "monetary"
    score_column = "RFM_Score" if "RFM_Score" in rfm.columns else "RFM_score"
    segment_column = "Segment" if "Segment" in rfm.columns else "segment"
    hover_columns = [column for column in ["customer_name", "frequency", score_column] if column in rfm.columns]
    fig = px.scatter(
        rfm,
        x="recency_days",
        y=monetary_column,
        color=segment_column,
        size="frequency",
        hover_data=hover_columns,
        title=title,
        labels={
            "recency_days": "Päevi viimasest ostust",
            monetary_column: "Kogukulutus (EUR)",
            "frequency": "Ostude arv",
        },
        category_orders={segment_column: SEGMENT_ORDER},
    )
    return fig


def city_chart(cities: pd.DataFrame, title: str) -> go.Figure:
    """Create city revenue chart."""
    fig = px.bar(
        cities.sort_values("revenue", ascending=True),
        x="revenue",
        y="city",
        orientation="h",
        text="revenue",
        title=title,
        labels={"revenue": "Tulu (EUR)", "city": "Linn"},
    )
    fig.update_traces(texttemplate="%{text:.0f} EUR", textposition="outside")
    fig.update_layout(margin={"l": 100, "r": 35, "t": 60, "b": 45})
    return fig


def monthly_chart(monthly: pd.DataFrame, title: str) -> go.Figure:
    """Create monthly revenue chart."""
    month_column = "month" if "month" in monthly.columns else "sale_date"
    fig = px.line(
        monthly,
        x=month_column,
        y="revenue",
        markers=True,
        title=title,
        labels={month_column: "Kuu", "revenue": "Tulu (EUR)"},
    )
    fig.update_traces(line={"width": 3})
    fig.update_layout(hovermode="x unified")
    return fig


def add_if_data(figures: list[go.Figure], dataframe: pd.DataFrame | None, builder, *args: str) -> None:
    """Append a figure only when the source CSV exists and has rows."""
    if dataframe is not None and not dataframe.empty:
        figures.append(builder(dataframe, *args))


def build_figures() -> list[go.Figure]:
    """Build all available Week 8 figures."""
    figures: list[go.Figure] = []

    team_weekly = read_latest(TEAM_OUTPUT, "weekly_aggregates_*.csv")
    team_monthly = read_latest(TEAM_OUTPUT, "monthly_report_*.csv")
    team_city = read_latest(TEAM_OUTPUT, "city_report_*.csv")
    team_kpis = read_latest(TEAM_OUTPUT, "kpis_*.csv")
    team_segments = read_latest(TEAM_OUTPUT, "rfm_segment_summary_*.csv")
    team_rfm = read_latest(TEAM_OUTPUT, "rfm_segments_*.csv")

    individual_weekly = read_latest(INDIVIDUAL_OUTPUT, "weekly_aggregates_*.csv")
    individual_kpis = read_latest(INDIVIDUAL_OUTPUT, "kpi_summary_*.csv")
    individual_segments = read_latest(INDIVIDUAL_OUTPUT, "rfm_segment_summary_*.csv")

    city = read_latest(PIPELINE_OUTPUT, "city_report_*.csv")
    monthly = read_latest(PIPELINE_OUTPUT, "monthly_report_*.csv")
    pipeline_rfm = read_latest(PIPELINE_OUTPUT, "rfm_report_*.csv")

    add_if_data(figures, team_kpis, kpi_table, "Tiimitöö: KPI kokkuvõte")
    add_if_data(figures, team_weekly, weekly_chart, "Tiimitöö: nädalane tulu")
    add_if_data(figures, team_monthly, monthly_chart, "Tiimitöö: kuukäive")
    add_if_data(figures, team_city, city_chart, "Tiimitöö: käive linnade lõikes")
    add_if_data(figures, team_segments, segment_chart, "Tiimitöö: RFM segmentide jaotus")
    add_if_data(figures, team_rfm, rfm_scatter, "Tiimitöö: RFM kliendisegmendid")
    add_if_data(figures, team_rfm, top_customers_chart, "Tiimitöö: top 10 klienti")

    add_if_data(figures, individual_kpis, kpi_table, "Individuaalne töö: KPI kokkuvõte")
    add_if_data(figures, individual_weekly, weekly_chart, "Individuaalne töö: nädalane tulu")
    add_if_data(figures, individual_segments, segment_chart, "Individuaalne töö: RFM segmentide jaotus")

    add_if_data(figures, city, city_chart, "API demo: käive linnade lõikes")
    add_if_data(figures, monthly, monthly_chart, "API demo: kuukäive")
    add_if_data(figures, pipeline_rfm, rfm_scatter, "API pipeline: RFM kliendisegmendid")
    add_if_data(figures, pipeline_rfm, top_customers_chart, "API pipeline: top 10 klienti")

    return figures


def render_figures(figures: Iterable[go.Figure]) -> str:
    """Render figures as Plotly HTML snippets with the library included once."""
    snippets: list[str] = []
    for index, fig in enumerate(figures):
        snippets.append(
            f'<section class="chart">{fig.to_html(full_html=False, include_plotlyjs=index == 0)}</section>'
        )
    return "\n".join(snippets)


def build_dashboard() -> Path:
    """Write the combined Week 8 dashboard."""
    figures = build_figures()
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    body = render_figures(figures)
    html = f"""<!doctype html>
<html lang="et">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Week 8 visuaalide koondleht</title>
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
      margin: 0 0 8px;
      font-size: 30px;
      font-weight: 700;
    }}
    p {{
      margin: 0;
      color: #52606d;
    }}
    .chart {{
      background: #ffffff;
      border: 1px solid #d9e2ec;
      border-radius: 8px;
      padding: 12px;
      overflow: hidden;
    }}
    @media (max-width: 720px) {{
      header,
      main {{
        padding-left: 14px;
        padding-right: 14px;
      }}
      h1 {{
        font-size: 24px;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Week 8 visuaalide koondleht</h1>
    <p>Tiimitöö, individuaalne töö ja API pipeline ühel lehel. Loodud: {generated_at}</p>
  </header>
  <main>
    {body}
  </main>
</body>
</html>
"""
    COMBINED_OUTPUT.write_text(html, encoding="utf-8")
    return COMBINED_OUTPUT


def main() -> None:
    """CLI entry point."""
    path = build_dashboard()
    print(f"Koondleht loodud: {path}")


if __name__ == "__main__":
    main()
