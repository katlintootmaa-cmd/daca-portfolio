# Week 8 Individual Work: Role C

Estonian version: [README.md](README.md)

## My Role

My subtask was **Visualization + Saving**. The goal of Role C was to create Plotly visualizations from the processed data and save the results as files that Marko can share with the team.

## File

- `visualize_export.py` - contains visualization and export functions.

## Functions

- `create_weekly_chart(df_weekly)` - creates a weekly revenue line chart.
- `create_kpi_summary(kpis)` - creates a KPI summary as a table.
- `create_segment_chart(df_segments)` - adds an RFM segment distribution chart.
- `export_results(results, output_dir)` - saves CSV and HTML files with a timestamp based on the team pipeline results.
- `export_results(df_weekly, kpis, output_dir, df_segments)` - also works with the old individual Role C input format.

## Running

```bash
.\.venv\Scripts\python.exe week-08/individual/visualize_export.py
```

When run, the file uses a small sample dataset and creates outputs in the folder:

```text
week-08/individual/output/
```

The module is also suitable for exporting Week 8 team pipeline results because `export_results()` can accept the same `results` dictionary that contains `weekly`, `kpis`, and `segment_summary`.

## Outputs

- `weekly_aggregates_*.csv`
- `kpi_summary_*.csv`
- `weekly_revenue_*.html`
- `kpi_summary_*.html`
- `rfm_segment_summary_*.csv`
- `rfm_segment_chart_*.html`

## How AI Helped

AI helped turn the Role C requirements from the guide into a concrete Python module: chart functions, timestamped export, and an independent test run with sample data.
