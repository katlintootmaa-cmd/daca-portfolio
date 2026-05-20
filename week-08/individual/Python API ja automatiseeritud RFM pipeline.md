# Nädal 8: Python API ja automatiseeritud RFM pipeline

## Töö eesmärk

Selle iseseisva töö eesmärk oli muuta Week 7 RFM analüüs automatiseeritud ETL pipeline'iks. Lahendus toob andmed Supabase Python API kaudu või kasutab vajadusel juhendi näidisandmeid, puhastab sisendi, arvutab linna- ja nädalakokkuvõtted, teeb RFM segmenteerimise ning salvestab CSV ja HTML raportid.

## Failid

- `individual/week8_api_pipeline.py` - käivitatav Python pipeline.
- `individual/logs/week8_pipeline.log` - logifail, mis tekib skripti käivitamisel.
- `individual/output/` - automaatselt loodud CSV ja Plotly HTML väljundid.

## Käivitamine

Supabase API-ga:

```bash
python week-08/individual/week8_api_pipeline.py
```

Näidisandmetega:

```bash
python week-08/individual/week8_api_pipeline.py --sample
```

Skript loeb `.env` failist `SUPABASE_URL` ja `SUPABASE_KEY` või `SUPABASE_ANON_KEY`. Kui ühendust või võtmeid ei ole, kasutab lahendus kontrollitavaid näidisandmeid.

## Harjutuste vastused

### Osa 1: API päringud

Viis A ehk CSV eksport nõuab mitu käsitsi sammu: dashboardi avamine, faili eksport, salvestamine ja Pythonis lugemine. Viis B ehk API päring vajab pärast seadistamist null käsitsi andmesamme, sest Python küsib värske andmestiku otse Supabase'ist.

Automatiseerimiseks sobib API, sest andmed on värsked ja skripti saab käivitada ajastatult. API tasemel filtreerimine on kasulik suure andmemahu korral, sest üle võrgu liigub vähem ridu ja pandas ei pea kõike mällu laadima.

### Osa 2: funktsioonid

`report_date` on `weekly_sales_report()` funktsiooni valikuline parameeter. Kui seda ei anta, kasutab funktsioon tänast kuupäeva. Nii saab sama funktsiooni kasutada nii igapäevasel käivitusel kui ka ajaloolise raporti taastootmisel.

Tühja DataFrame'i korral tagastab raport `avg_order` väärtuseks `0.0`, et skript ei kukuks `NaN` või jagamisprobleemide tõttu kokku. RFM funktsioon tagastab tühja DataFrame'i, kui sisend on tühi.

### Osa 3: pipeline

Pipeline'i struktuur:

- EXTRACT: toob `sales` ja `customers` tabelid Supabase API kaudu või loob näidisandmed.
- TRANSFORM: puhastab kuupäevad ja summad, arvutab linnaraporti, nädalakokkuvõtte, kuukäibe ja RFM segmendid.
- VALIDATE: kontrollib, et andmed ei ole tühjad, käive on positiivne ja kuukäive klapib kogukäibega.
- LOAD: salvestab CSV raportid ja Plotly HTML graafikud.

Pipeline lahendab Marko probleemi, sest sama raportit ei pea enam iga nädal käsitsi CSV failidest kokku panema. Logimine näitab hiljem, millises etapis viga tekkis.

## Päris API käivituse tulemus

Pipeline õnnestus käivitada Supabase API vastu. Tulemused:

- Laaditi `sales` tabelist 10118 rida ja `customers` tabelist 3150 rida.
- Pärast puhastamist jäi analüüsi 8950 müügirida.
- Kogukäive oli 2676850.54 EUR.
- Unikaalseid kliente oli 2540.
- RFM tuvastas 4 segmenti.
- Kõige väärtuslikum klient oli `customer_id` 3618, monetary 27920.86 EUR.
- Kõige kasumlikum kuu oli 2024-12, käive 156588.00 EUR.
- Linnade käive: Tallinn 1006092.81 EUR, Online 929622.82 EUR, Tartu 472884.31 EUR, Pärnu 268250.60 EUR.


## Minu kokkuvõte

Kõige olulisem õppimiskoht oli see, et API ja pipeline teevad sama analüüsi korratavaks. Pandas annab arvutused, Supabase API annab värsked andmed ja ETL struktuur paneb töö loogilisteks sammudeks, mida saab hiljem ajastada näiteks GitHub Actionsi või croniga.
