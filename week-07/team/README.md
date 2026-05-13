# Nädal 7 tiimitöö: RFM kliendisegmenteerimine

## Failid

- `week7_rfm_complete.ipynb` - terviklik grupitöö notebook rollidega A, B, C ja D.
- `rfm_segments.csv` - Supabase andmetest eksporditud kliendisegmendid turundusmeeskonnale.

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


