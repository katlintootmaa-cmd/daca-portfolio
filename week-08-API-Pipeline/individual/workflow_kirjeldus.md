# Week 8 individuaalse pipeline'i töökäigu kirjeldus

## Eesmärgid

Individuaalse töö eesmärk oli muuta varasem RFM analüüs automaatseks Python pipeline'iks. Selle asemel, et andmeid käsitsi CSV failidest kokku panna, küsib skript andmed Supabase API kaudu, puhastab need, arvutab aruanded ja salvestab tulemused failidena.

Pipeline asub failis:

```text
week-08/individual/week8_api_pipeline.py
```

## 1. Ettevalmistus

Enne pipeline'i käivitamist peavad vajalikud Python paketid olema paigaldatud. Skript kasutab peamiselt:

- `pandas` andmete töötlemiseks
- `plotly` HTML graafikute loomiseks
- `python-dotenv` `.env` faili lugemiseks
- `supabase` API ühenduse loomiseks

Supabase ühenduse jaoks loetakse projekti `.env` failist:

```text
SUPABASE_URL
SUPABASE_KEY
```

Kui API võtmeid või ühendust ei ole, proovib skript kasutada kohalikke CSV fallback-faile.

## 2. Extract ehk andmete laadimine

Extract etapis kutsub pipeline välja `extract()` funktsiooni. See proovib luua Supabase kliendi ning laadida andmed tabelitest:

- `sales`
- `customers`

Andmeid ei eeldata ühes vastuses. Funktsioon `fetch_table()` kasutab lehekülgede kaupa laadimist `range(start, end)` abil, et kätte saada ka suuremad tabelid.

Kui Supabase API ei ole saadaval või tagastab puudulikud andmed, kasutab pipeline fallback-loogikat ning otsib CSV faile kohalikest kaustadest.

## 3. Transform ehk andmete puhastamine ja arvutused

Transform etapis kutsub pipeline välja `transform()` funktsiooni. Selle sees tehakse mitu andmetöötluse sammu.

Esiteks ühtlustab `normalize_orders()` veerud nii, et pipeline töötaks nii API kui CSV andmetega. Näiteks kontrollitakse kuupäeva, kliendi, linna ja müügisumma veerge.

Seejärel puhastatakse andmed:

- eemaldatakse puuduvate kohustuslike väärtustega read
- teisendatakse `sale_date` kuupäevaformaati
- teisendatakse `total_price` numbriks
- eemaldatakse negatiivsed või nullväärtusega müügiread
- filtreeritakse andmed analüüsi lõppkuupäevani
- alles jäetakse kliendid, kellel on e-mail või telefon olemas

Pärast puhastamist arvutatakse:

- linnade müügiraport `city_report()`
- nädalane kokkuvõte `weekly_sales_report()`
- kuukäive `monthly_report()`
- RFM segmendid `calculate_rfm()`

RFM analüüsis kasutatakse kolme näitajat:

- Recency: mitu päeva on viimasest ostust möödas
- Frequency: mitu ostu klient on teinud
- Monetary: kui palju klient on kokku kulutanud

Nende põhjal arvutatakse R, F ja M skoorid ning määratakse kliendisegment.

## 4. Validate ehk tulemuste kontroll

Validate etapis kontrollib `validate()` funktsioon, et pipeline'i tulemused on kasutatavad.

Kontrollitakse, et:

- puhastatud tellimuste tabel ei ole tühi
- RFM raport ei ole tühi
- kogukäive on positiivne
- kuukäivete summa klapib puhastatud tellimuste kogukäibega

Kui kõik kontrollid on korras, liigub pipeline edasi salvestamise etappi. Kui mõni kontroll ebaõnnestub, katkestab skript töö ja annab veateate.

## 5. Load ehk tulemuste salvestamine

Load etapis kutsub pipeline välja `load()` funktsiooni. See loob vajadusel `output` kausta ning salvestab tulemused ajatempliga failidesse.

Väljundid salvestatakse kausta:

```text
week-08/individual/output/
```

Loodavad failid:

- `rfm_report_*.csv`
- `city_report_*.csv`
- `monthly_report_*.csv`
- `rfm_chart_*.html`
- `monthly_chart_*.html`

CSV failid sobivad andmete kontrollimiseks ja edasi töötlemiseks. HTML failid sisaldavad Plotly graafikuid, mida saab avada brauseris.

## 6. Logimine

Pipeline kasutab logimist, et iga etapi tegevused oleksid hiljem kontrollitavad.

Logifailid tekivad kausta:

```text
week-08/individual/logs/
```

Peamised logid:

- `week8_pipeline.log` - tavapärane käivituse logi
- `week8_pipeline_errors.log` - veateated

Logidest on näha, mitu rida API kaudu laaditi, millised kontrollid läbiti ja kas väljundite salvestamine õnnestus.

## 7. Käivitamine

Pipeline'i saab käivitada projekti juurkaustast:

```bash
python week-08/individual/week8_api_pipeline.py
```

Vaikimisi kasutab skript analüüsi lõppkuupäevana `2025-02-28`.

Teise lõppkuupäeva saab anda käsurealt:

```bash
python week-08/individual/week8_api_pipeline.py --date 2025-03-01
```

## Kokkuvõte

See töökäik teeb RFM analüüsi korratavaks. Andmed laetakse API kaudu, puhastatakse kindlate reeglite alusel, tulemused kontrollitakse ning raportid salvestatakse automaatselt. Sellist lahendust saab hiljem kasutada korduvate nädalaste raportite loomiseks või ajastada automaatselt käivituma.

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
