# UrbanStyle API Pipeline'i Visualiseerimine ja Eksport

English version: [README_EN.md](README_EN.md)

## Äriprobleem

UrbanStyle'i pipeline pidi muutma töödeldud andmed jagatavateks väljunditeks. Ainult andmetabelitest ei piisa, sest meeskond vajab graafikuid, KPI kokkuvõtteid ja faile, mida saab korduvkasutatavalt salvestada.

## Lähenemine

Minu alaülesanne oli **Visualization + Saving**. Roll C eesmärk oli teha töödeldud andmetest Plotly visualisatsioonid ja salvestada tulemused failidena, mida Marko saab jagada meeskonnaga.

## Peamised leiud

- Pipeline'i väljund peab olema automaatselt salvestatav, et tulemusi saaks hiljem kontrollida ja jagada.
- Ajatempliga failinimed aitavad vältida varasemate tulemuste ülekirjutamist.
- Sama `export_results()` funktsioon peab toetama nii tiimi pipeline'i tulemuste sõnastikku kui ka varasemat individuaalset sisendkuju.

## Tehniline pinurida

- Python
- Pandas
- Plotly
- CSV ja HTML eksport

## Funktsioonid

- `create_weekly_chart(df_weekly)` - loob nädalase tulu joondiagrammi.
- `create_kpi_summary(kpis)` - loob KPI kokkuvõtte tabelina.
- `create_segment_chart(df_segments)` - lisab RFM segmentide jaotuse graafiku.
- `export_results(results, output_dir)` - salvestab tiimi pipeline'i tulemuste põhjal CSV ja HTML failid ajatempliga.
- `export_results(df_weekly, kpis, output_dir, df_segments)` - töötab ka vana iseseisva Roll C sisendkujuga.

## Kuidas käivitada

```bash
.\.venv\Scripts\python.exe week-08-API-Pipeline\individual\visualize_export.py
```

Käivitamisel kasutab fail väikest näidisandmestikku ja loob väljundid kausta:

```text
week-08-API-Pipeline/individual/output/
```

Moodul sobib ka Week 8 tiimi pipeline'i tulemuste ekspordiks, sest `export_results()` oskab vastu võtta sama `results` sõnastikku, kus on `weekly`, `kpis` ja `segment_summary`.

## Ekraanipildid ja väljundid

- `weekly_aggregates_*.csv`
- `kpi_summary_*.csv`
- `weekly_revenue_*.html`
- `kpi_summary_*.html`
- `rfm_segment_summary_*.csv`
- `rfm_segment_chart_*.html`

Visuaalne koondväljund:

- [combined_visuals.html](combined_visuals.html)
- [combined_visuals_screenshot.png](combined_visuals_screenshot.png)

## Õpitu ja väljakutsed

Suurim väljakutse oli teha ekspordifunktsioon piisavalt paindlikuks, et see töötaks nii individuaalse testandmestiku kui ka tiimi pipeline'i tulemusega. Õppisin, et automatiseeritud väljundid vajavad selget failinimede loogikat ja kontrollitavat kaustastruktuuri.

## AI kasutamine

AI aitas juhendi Roll C nõuded muuta konkreetseks Python mooduliks: diagrammifunktsioonid, ajatempliga eksport ja iseseisev testkäivitus näidisandmetega. Lõplik funktsioonide ülesehitus, väljundite kontroll ja seos tiimi pipeline'iga on minu töö.
