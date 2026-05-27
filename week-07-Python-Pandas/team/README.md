# Nädal 7 tiimitöö: RFM kliendisegmenteerimine

## Failid

- `week7_rfm_complete.ipynb` - terviklik grupitöö notebook rollidega A, B, C ja D.
- `rfm_segments.csv` - Supabase andmetest eksporditud kliendisegmendid turundusmeeskonnale.
- `rfm_segmentide_jaotus.png`, `rfm_segmentide_scatter.png`, `rfm_top_10_vip.png` - RFM tulemuste visuaalid.

## Andmeallikas

Notebook kasutab Supabase ühendust `.env` failist:

```python
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
```

Vajalikud paketid on projekti `.venv` keskkonnas olemas. Notebooki avamisel vali kerneliks projekti virtuaalkeskkond.

## Rollid

- Roll A: laeb `sales` ja `customers` tabelid Supabase'ist ning teeb merge'i `customer_id` põhjal.
- Roll B: puhastab andmed, eemaldab duplikaadid, NULL-id, vigased kuupäevad ja mittepositiivsed summad.
- Roll C: arvutab Recency, Frequency ja Monetary väärtused ning määrab RFM segmendid.
- Roll D: loob kolm Plotly diagrammi ja sõnastab soovitused Markole.

## Kuupäevapiirang

Analüüs kasutab RFM võrdluskuupäevana `2025-02-28` ja filtreerib RFM sisendist välja kõik hilisemad müügiread. Nii arvestab Week 7 töö andmeid kuni 2025. aasta veebruari lõpuni.

## Analüütiline tõlgendus

Week 7 on RFM-analüüsi aluskiht: see näitab, millised kliendid ostsid hiljuti, ostsid sageli ja tõid suurimat käivet. Segmentide äriline mõte on järgmine:

- `VIP Champions`: hoia neid kliente personaalse suhtluse, early access pakkumiste ja lojaalsusprogrammi erikohtlemisega.
- `Loyal`: kasvata keskmist ostukorvi cross-sell ja bundle pakkumistega.
- `Potential`: suuna neid teisele ja kolmandale ostule, et nad liiguksid lojaalsemaks segmendiks.
- `At Risk`: käivita win-back kampaania enne, kui kliendid liiguvad kadunud segmenti.
- `Lost`: testi madala kuluga taasaktiveerimist ja hoia kampaania ROI kontrolli all.

## Soovitatud järgmised sammud

- Lisa iga segmendi juurde konkreetne kampaania eesmärk, kanal, pakkumine ja mõõdik.
- Võrdle segmente linna, kanali ja tootekategooria lõikes.
- Mõõda kampaaniaid kontrollgrupiga, mitte ainult enne/pärast võrdlusega.
- Jätka Week 8 pipeline'is sama loogikat automatiseeritud raporti, cohort retentioni ja A/B testiplaaniga.
