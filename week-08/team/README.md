# Week 8 tiimitöö: Python API pipeline

See kaust sisaldab Week 8 grupitöö modulaarset pipeline'i. Lahendus muudab Week 7 RFM analüüsi API kaudu käivitatavaks ja automatiseeritavaks ning lisab marketingi otsustuskihi.

Fail `week-08/individual/week8_api_pipeline.py` on jäetud individuaalseks demo-/arhiiviversiooniks. Tiimitöö hooldatav pipeline asub siin kaustas.

## Rollid ja failid

- `data_fetcher.py` - Roll A: Supabase API päringud (`fetch_sales`, `fetch_customers`, `fetch_products`), pagination, retry ja fallback.
- `transform.py` - Roll B: puhastamine, ühendamine, KPI-d, RFM, cohort retention ja kampaaniaplaan.
- `visualize_export.py` - Roll C: Plotly graafikud, executive dashboard ja HTML visuaalide eksport.
- `pipeline.py` - Roll D: orkestreerib kogu protsessi `extract -> transform -> validate -> export -> notify`.
- `notifications.py` - valikulised webhooki ja emaili teavitused.
- `config.yaml` - kuupäevafiltrid, tabelinimed, retry, output kaust ja RFM võrdluskuupäev.
- `tests/` - väikesed kontrollid RFM ja marketing-analüütika loogikale.

## Käivitamine

Projekti virtuaalkeskkonnaga:

```bash
.\.venv\Scripts\python.exe week-08/team/pipeline.py
```

Kui virtuaalkeskkond on aktiveeritud:

```bash
python week-08/team/pipeline.py
```

Valikulise analüüsi lõppkuupäevaga:

```bash
python week-08/team/pipeline.py --date 2025-02-28
```

API jaoks peavad projekti `.env` failis olema:

```text
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
```

Kui API ühendus puudub või Supabase on maas, kasutab pipeline `config.yaml` seadistuse järgi kohalikke CSV fallback andmeid või näidisandmeid. Dashboard ja teavitus näitavad kasutatud andmeallikat.

## Mida pipeline teeb

1. Pärib Supabase API-st müügi-, kliendi- ja tooteandmed.
2. Kasutab kuupäevafiltrit kuni `2025-02-28`, et analüüs arvestaks andmeid kuni 2025. aasta veebruari lõpuni.
3. Kasutab pagination'i, et kätte saada rohkem kui 1000 rida.
4. Kasutab retry loogikat API päringutele ja pipeline'i etappidele.
5. Liidab andmestikud `customer_id` ja võimalusel `product_id` alusel.
6. Puhastab duplikaadid, vigased kuupäevad, tühjad kliendid ja mittepositiivsed summad.
7. Arvutab nädala-, kuu-, linna- ja kanaliraportid.
8. Arvutab KPI-d, RFM segmentatsiooni ja cohort retentioni.
9. Koostab segmentide tootekategooria profiili ja kampaaniaplaani.
10. Ekspordib Plotly HTML graafikud ja koonddashboardi.

## Väljundid

`output/` kausta tekivad ainult ajatempliga HTML visuaalid:
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

HTML visuaalidele tehakse ka stabiilsed `*_latest` koopiad, näiteks `team_dashboard_latest.html`, `weekly_revenue_latest.html` ja `kpi_summary_latest.html`.

## RFM segmentide loogika

- `13-15` punkti: `VIP Champions`
- `10-12` punkti: `Loyal`
- `7-9` punkti: `Potential`
- `4-6` punkti: `At Risk`
- alla `4` punkti: `Lost`

## Marketingi parimad praktikad

- RFM segmentatsiooni kasutatakse koos kampaaniaplaaniga: igal segmendil on eesmärk, sõnum, kanal, pakkumine ja mõõdik.
- Cohort retention näitab, kas probleem on uute klientide hoidmine või vanade klientide kadumine.
- Kampaaniaplaan seob iga RFM segmendi eesmärgi, sõnumi, kanali, pakkumise ja mõõdikuga.
- Dashboard ei kuva enam kliendi emaili ega telefoni RFM hover-infona; kontaktandmed jäävad CSV-sse sisemiseks kasutuseks.

## Teavitused

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

Teavitus sisaldab pipeline'i staatust, kestust, väljundkausta, andmeallikat ning KPI tabelit.

## Testid

```bash
python -m pytest week-08/team/tests
```

## Süntees Markole

Pipeline hoiab kokku käsitsi töötluse aega, sest sama protsess käivitub ühe käsuga: API päring, puhastamine, KPI-d, RFM, marketingi tegevusplaan, graafikud ja eksport. Kui Supabase on maas, logib pipeline vea, proovib päringut uuesti ja kasutab vajadusel varuandmeid, kuid teeb selle raportis nähtavaks.

## AI kasutamine

AI aitas Week 7 notebooki loogika muuta Week 8 juhendile vastavaks moodulipõhiseks API pipeline'iks ning lisada retry, logimise, valideerimise, ekspordi, marketingi mõõtmise ja testimise sammud.
