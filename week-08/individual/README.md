# Week 8 individuaalne töö: Roll C

## Minu roll

Minu alaülesanne oli **Visualization + Saving**. Roll C eesmärk oli teha töödeldud andmetest Plotly visualisatsioonid ja salvestada tulemused failidena, mida Marko saab jagada meeskonnaga.

## Fail

- `visualize_export.py` - sisaldab visualiseerimise ja ekspordi funktsioone.

## Funktsioonid

- `create_weekly_chart(df_weekly)` - loob nädalase tulu joondiagrammi.
- `create_kpi_summary(kpis)` - loob KPI kokkuvõtte tabelina.
- `create_segment_chart(df_segments)` - lisab RFM segmentide jaotuse graafiku.
- `export_results(df_weekly, kpis, output_dir, df_segments)` - salvestab CSV ja HTML failid ajatempliga.

## Käivitamine

```bash
.\.venv\Scripts\python.exe week-08/individual/visualize_export.py
```

Käivitamisel kasutab fail väikest näidisandmestikku ja loob väljundid kausta:

```text
week-08/individual/output/
```

## Väljundid

- `weekly_aggregates_*.csv`
- `kpi_summary_*.csv`
- `weekly_revenue_*.html`
- `kpi_summary_*.html`
- `rfm_segment_summary_*.csv`
- `rfm_segment_chart_*.html`

## Kuidas AI aitas

AI aitas juhendi Roll C nõuded muuta konkreetseks Python mooduliks: diagrammifunktsioonid, ajatempliga eksport ja iseseisev testkäivitus näidisandmetega.
