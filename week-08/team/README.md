# Week 8 tiimitöö: Python API pipeline

See kaust sisaldab Week 8 grupitöö juhendi järgi tehtud modulaarset pipeline'i. Lahendus muudab Week 7 RFM analüüsi API kaudu käivitatavaks ja automatiseeritavaks.

See on projekti põhiline hooldatav pipeline. Fail `week-08/individual/week8_api_pipeline.py` on jäetud individuaalseks demo-/arhiiviversiooniks.

## Rollid ja failid

- `data_fetcher.py` - Roll A: Supabase API päringud (`fetch_sales`, `fetch_customers`, `fetch_products`).
- `transform.py` - Roll B: andmete puhastamine, ühendamine, nädalased koondnäitajad, KPI-d ja RFM.
- `visualize_export.py` - Roll C: Plotly graafikud ja CSV/HTML/Markdown eksport.
- `pipeline.py` - Roll D: orkestreerib kogu protsessi `extract -> transform -> validate -> export`.
- `config.yaml` - konfiguratsioon: kuupäevafiltrid, retry, output kaust, RFM võrdluskuupäev.
- `logs/` - failipõhised logid tekivad käivitamisel.
- `output/` - väljundfailid tekivad käivitamisel.

## Käivitamine

Projekti virtuaalkeskkonnaga:

```bash
.\.venv\Scripts\python.exe week-08/team/pipeline.py
```

Kui virtuaalkeskkond on aktiveeritud:

```bash
python week-08/team/pipeline.py
```

API jaoks peavad projekti `.env` failis olema:

```text
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
```

Kui API ühendus puudub või Supabase on maas, kasutab pipeline `config.yaml` seadistuse järgi näidisandmeid, et protsess saaks lõpuni joosta ja väljundfailid tekiksid.

## Mida pipeline teeb

1. Pärib Supabase API-st müügi-, kliendi- ja tooteandmed.
2. Kasutab kuupäevafiltrit kuni `2025-02-28`, et analüüs arvestaks andmeid kuni 2025. aasta veebruari lõpuni.
3. Kasutab pagination'i, et kätte saada rohkem kui 1000 rida.
4. Kasutab retry loogikat, kui API päring ebaõnnestub.
5. Liidab andmestikud `customer_id` ja võimalusel `product_id` alusel.
6. Puhastab duplikaadid, vigased kuupäevad, tühjad kliendid ja mittepositiivsed summad.
7. Arvutab nädalased koondnäitajad ja KPI-d.
8. Arvutab Week 7 RFM segmentatsiooni.
9. Ekspordib CSV failid, Plotly HTML graafikud ja äriraporti.

## Väljundid

`output/` kausta tekivad ajatempliga failid:

- `weekly_aggregates_*.csv`
- `monthly_report_*.csv`
- `city_report_*.csv`
- `kpis_*.csv`
- `rfm_segments_*.csv`
- `rfm_segment_summary_*.csv`
- `rfm_business_report_*.md`
- `weekly_revenue_*.html`
- `monthly_revenue_*.html`
- `city_revenue_*.html`
- `kpi_summary_*.html`
- `rfm_segmentide_jaotus_*.html`
- `rfm_segmentide_scatter_*.html`
- `rfm_top_10_vip_*.html`
- `team_dashboard_*.html`

## Edasijõudnute teavitus

Pipeline saadab õnnestumise või ebaõnnestumise teavituse, kui `.env` failis on seadistatud vähemalt üks kanal:

```text
NOTIFY_WEBHOOK_URL=...
```

või SMTP email:

```text
SMTP_HOST=...
SMTP_PORT=587
SMTP_USER=...
SMTP_PASSWORD=...
SMTP_FROM=...
NOTIFY_EMAIL_TO=marko@example.com
```

Teavitus sisaldab pipeline'i staatust, kestust, väljundkausta ning KPI numbreid: kogutulu, tellimuste arv, unikaalsed kliendid ja keskmine tellimus.
Emaili puhul lisatakse manustena CSV raportid ja `team_dashboard_*.html` koondvisuaalidega.

## RFM segmentide loogika

- `13-15` punkti: `VIP Champions`
- `10-12` punkti: `Loyal`
- `7-9` punkti: `Potential`
- `4-6` punkti: `At Risk`
- alla `4` punkti: `Lost`

## Süntees Markole

Pipeline hoiab kokku käsitsi töötluse aega, sest sama protsess käivitub ühe käsuga: API päring, puhastamine, KPI-d, RFM, graafikud ja eksport. Kui Supabase on maas, logib pipeline vea, proovib päringut uuesti ja kasutab vajadusel varuandmeid, et demo ja raport ei jääks pooleli.

## AI kasutamine

AI aitas Week 7 notebooki loogika muuta Week 8 juhendile vastavaks moodulipõhiseks API pipeline'iks ning lisada retry, logimise, valideerimise ja ekspordi sammud.
