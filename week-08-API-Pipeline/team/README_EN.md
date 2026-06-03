# Week 8 Team Work: Python API Pipeline

Estonian version: [README.md](README.md)

This folder contains the modular pipeline for the Week 8 group work. The solution turns the Week 7 RFM analysis into an API-driven and automatable workflow and adds a marketing decision layer.

The file `week-08/individual/week8_api_pipeline.py` is kept as an individual demo/archive version. The maintainable team pipeline is located in this folder.

## Roles and Files

- `data_fetcher.py` - Role A, Karmo: Supabase API queries (`fetch_sales`, `fetch_customers`, `fetch_products`), pagination, retry, and fallback.
- `transform.py` - Role B, Mari: cleaning, joining, KPIs, RFM, cohort retention, and campaign plan.
- `visualize_export.py` - Role C, Kätlin: Plotly charts, executive dashboard, and HTML visual export.
- `pipeline.py` - Role D, Ragnar: orchestrates the full process `extract -> transform -> validate -> export -> notify`.
- `notifications.py` - optional webhook and email notifications.
- `config.yaml` - date filters, table names, retry, output folder, and RFM reference date.
- `tests/` - small checks for RFM and marketing analytics logic.

## Role Descriptions

- Role A, the API data query developer, was responsible for getting data through the Supabase API. The focus was `data_fetcher.py`, pagination, retry, and fallback so that the pipeline would not stop at the first connection problem.
- Role B, the transformation developer, was responsible for data cleaning, joining, and analytics calculations. The focus was `transform.py`, KPIs, RFM segmentation, cohort retention, and campaign plan.
- Role C, the visualization and export developer, was responsible for making pipeline results readable and shareable. The focus was `visualize_export.py`, Plotly charts, HTML export, and the executive dashboard.
- Role D, the pipeline orchestrator, was responsible for connecting the full workflow. The focus was `pipeline.py`, so that extract, transform, validate, export, and notify stages work with one command.

## Running

With the project virtual environment:

```bash
.\.venv\Scripts\python.exe week-08/team/pipeline.py
```

If the virtual environment is activated:

```bash
python week-08/team/pipeline.py
```

With an optional analysis end date:

```bash
python week-08/team/pipeline.py --date 2025-02-28
```

For the API, the project `.env` file must contain:

```text
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
```

If the API connection is missing or Supabase is down, the pipeline uses local CSV fallback data or sample data according to the `config.yaml` settings. The dashboard and notification show which data source was used.

## What the Pipeline Does

1. Requests sales, customer, and product data from the Supabase API.
2. Uses the date filter up to `2025-02-28`, so the analysis includes data until the end of February 2025.
3. Uses pagination to fetch more than 1,000 rows.
4. Uses retry logic for API queries and pipeline stages.
5. Joins datasets by `customer_id` and, where possible, `product_id`.
6. Cleans duplicates, invalid dates, empty customers, and non-positive amounts.
7. Calculates weekly, monthly, city, and channel reports.
8. Calculates KPIs, RFM segmentation, and cohort retention.
9. Creates product category profiles and a campaign plan for segments.
10. Exports Plotly HTML charts and a summary dashboard.

## Outputs

The `output/` folder receives only timestamped HTML visuals:
- `weekly_revenue_*.html`
- `monthly_revenue_*.html`
- `city_revenue_*.html`
- `channel_revenue_*.html`
- `kpi_summary_*.html`
- `cohort_retention_*.html`
- `segment_category_profile_*.html`
- `marketing_campaign_plan_*.html`
- `rfm_segmentide_jaotus_*.html`
- `rfm_segmentide_scatter_*.html`
- `rfm_top_10_vip_*.html`
- `team_dashboard_*.html`

Stable `*_latest` copies are also created for HTML visuals, for example `team_dashboard_latest.html`, `weekly_revenue_latest.html`, and `kpi_summary_latest.html`.

## RFM Segment Logic

- `13-15` points: `VIP Champions`
- `10-12` points: `Loyal`
- `7-9` points: `Potential`
- `4-6` points: `At Risk`
- below `4` points: `Lost`

## Marketing Best Practices

- RFM segmentation is used together with the campaign plan: each segment has a goal, message, channel, offer, and metric.
- Cohort retention shows whether the problem is retaining new customers or losing old customers.
- The campaign plan connects each RFM segment with a goal, message, channel, offer, and metric.
- The dashboard no longer shows customer email or phone as RFM hover information; contact data stays in CSV for internal use.

## Notifications

The pipeline sends a success or failure notification if at least one channel is configured in the `.env` file:

```text
NOTIFY_WEBHOOK_URL=...
```

or SMTP email:

```text
SMTP_HOST=...
SMTP_PORT=587
SMTP_USER=...
SMTP_PASSWORD=...
SMTP_FROM=...
NOTIFY_EMAIL_TO=marko@example.com
```

The notification includes pipeline status, duration, output folder, data source, and KPI table.

## Tests

```bash
python -m pytest week-08/team/tests
```

## Synthesis for Marko

The pipeline saves manual processing time because the same process runs with one command: API query, cleaning, KPIs, RFM, marketing action plan, charts, and export. If Supabase is down, the pipeline logs the error, retries the query, and uses fallback data if needed, while making this visible in the report.

## AI Usage

AI helped turn the Week 7 notebook logic into a module-based API pipeline that matches the Week 8 instructions and add retry, logging, validation, export, marketing measurement, and testing steps.
