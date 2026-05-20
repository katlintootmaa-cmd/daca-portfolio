# Week 8 individuaalse pipeline'i tookaigu kirjeldus

## Eesmargid

Individuaalse too eesmargiks oli muuta varasem RFM analuus automaatseks Python pipeline'iks. Selle asemel, et andmeid kasitsi CSV failidest kokku panna, kusib skript andmed Supabase API kaudu, puhastab need, arvutab aruanded ja salvestab tulemused failidena.

Pipeline asub failis:

```text
week-08/individual/week8_api_pipeline.py
```

## 1. Ettevalmistus

Enne pipeline'i kaivitamist peavad vajalikud Python paketid olema paigaldatud. Skript kasutab peamiselt:

- `pandas` andmete tootlemiseks
- `plotly` HTML graafikute loomiseks
- `python-dotenv` `.env` faili lugemiseks
- `supabase` API uhenduse loomiseks

Supabase uhenduse jaoks loetakse projekti `.env` failist:

```text
SUPABASE_URL
SUPABASE_KEY
```

Kui API votmeid voi uhendust ei ole, proovib skript kasutada kohalikke CSV fallback-faile.

## 2. Extract ehk andmete laadimine

Extract etapis kutsub pipeline valja `extract()` funktsiooni. See proovib luua Supabase kliendi ning laadida andmed tabelitest:

- `sales`
- `customers`

Andmeid ei eeldata uhes vastuses. Funktsioon `fetch_table()` kasutab lehekulgede kaupa laadimist `range(start, end)` abil, et katte saada ka suuremad tabelid.

Kui Supabase API ei ole saadaval voi tagastab puudulikud andmed, kasutab pipeline fallback-loogikat ning otsib CSV faile kohalikest kaustadest.

## 3. Transform ehk andmete puhastamine ja arvutused

Transform etapis kutsub pipeline valja `transform()` funktsiooni. Selle sees tehakse mitu andmetootluse sammu.

Esiteks uhtlustab `normalize_orders()` veerud nii, et pipeline tootaks nii API kui CSV andmetega. Naiteks kontrollitakse kuupaeva, kliendi, linna ja muugisumma veerge.

Seejarel puhastatakse andmed:

- eemaldatakse puuduvate kohustuslike vaartustega read
- teisendatakse `sale_date` kuupaevaformaati
- teisendatakse `total_price` numbriks
- eemaldatakse negatiivsed voi nullvaartusega muugiread
- filtreeritakse andmed analyysi loppkuupaevani
- alles jaetakse kliendid, kellel on e-mail voi telefon olemas

Parast puhastamist arvutatakse:

- linnade muugiraport `city_report()`
- nadalane kokkuvote `weekly_sales_report()`
- kuukive `monthly_report()`
- RFM segmendid `calculate_rfm()`

RFM analuusis kasutatakse kolme naitajat:

- Recency: mitu paeva on viimasest ostust moodas
- Frequency: mitu ostu klient on teinud
- Monetary: kui palju klient on kokku kulutanud

Nende pohjal arvutatakse R, F ja M skoorid ning maaratakse kliendisegment.

## 4. Validate ehk tulemuste kontroll

Validate etapis kontrollib `validate()` funktsioon, et pipeline'i tulemused on kasutatavad.

Kontrollitakse, et:

- puhastatud tellimuste tabel ei ole tuhi
- RFM raport ei ole tuhi
- kogukaive on positiivne
- kuukivete summa klapib puhastatud tellimuste kogukaibega

Kui koik kontrollid on korras, liigub pipeline edasi salvestamise etappi. Kui moni kontroll ebaonnestub, katkestab skript too ja annab veateate.

## 5. Load ehk tulemuste salvestamine

Load etapis kutsub pipeline valja `load()` funktsiooni. See loob vajadusel `output` kausta ning salvestab tulemused ajatempliga failidesse.

Valjundid salvestatakse kausta:

```text
week-08/individual/output/
```

Loodavad failid:

- `rfm_report_*.csv`
- `city_report_*.csv`
- `monthly_report_*.csv`
- `rfm_chart_*.html`
- `monthly_chart_*.html`

CSV failid sobivad andmete kontrollimiseks ja edasi tootlemiseks. HTML failid sisaldavad Plotly graafikuid, mida saab avada brauseris.

## 6. Logimine

Pipeline kasutab logimist, et iga etapi tegevused oleksid hiljem kontrollitavad.

Logifailid tekivad kausta:

```text
week-08/individual/logs/
```

Peamised logid:

- `week8_pipeline.log` - tavapärane kaivituse logi
- `week8_pipeline_errors.log` - veateated

Logidest on naha, mitu rida API kaudu laaditi, millised kontrollid labiti ja kas valjundite salvestamine onnestus.

## 7. Kaivitamine

Pipeline'i saab kaivitada projekti juurkaustast:

```bash
python week-08/individual/week8_api_pipeline.py
```

Vaikimisi kasutab skript analyysi loppkuupaevana `2025-02-28`.

Teise loppkuupaeva saab anda kasurealt:

```bash
python week-08/individual/week8_api_pipeline.py --date 2025-03-01
```

## Kokkuvote

See tookaik teeb RFM analyysi korratavaks. Andmed laetakse API kaudu, puhastatakse kindlate reeglite alusel, tulemused kontrollitakse ning raportid salvestatakse automaatselt. Sellist lahendust saab hiljem kasutada korduvate nadalaste raportite loomiseks voi ajastada automaatselt kaivituma.

## Edasiarendus tiimitöö pipeline'is

Tiimitöö versioonis `week-08/team/pipeline.py` laiendati sama töövoogu marketingi parimate praktikatega:

- andmekvaliteedi raport enne ja pärast puhastamist;
- kanalianalüüs ja tootekategooria profiil RFM segmentide lõikes;
- cohort retention esimese ostukuu põhjal;
- lihtsustatud 6 kuu CLV hinnang;
- konkreetne kampaaniaplaan igale RFM segmendile;
- A/B testimise plaan kontrollgrupi ja mõõdikutega;
- stabiilsed `*_latest` väljundfailid, et viimast dashboardi oleks lihtne avada.

Need lisad muudavad pipeline'i tehnilisest automatiseerimisest turunduse otsustustööriistaks: raport ei ütle ainult, mis juhtus, vaid pakub ka järgmise kampaania, mõõtmise viisi ja edukriteeriumi.
