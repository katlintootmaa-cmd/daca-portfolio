# Nädal 8: Python API ja automatiseeritud andmepipeline

## Praegune failistruktuuri otsus

Põhiline hooldatav Week 8 pipeline on `week-08/team/pipeline.py`. See on modulaarne versioon, kus API päringud, transformatsioonid, eksport ja teavitused on eraldi failides.

`week-08/individual/week8_api_pipeline.py` on jäetud individuaalseks demo-/arhiiviversiooniks. Seda saab kasutada õppimiseks ja varasema lahenduse näitamiseks, aga edasised töökindlad muudatused tuleks teha `team/` kausta moodulites.

## Mida ma õppisin

Selle nädala iseseisvas töös õppisin, kuidas Pythoniga andmeid otse Supabase andmebaasist küsida. Varasemalt töötasin rohkem CSV-failide ja pandas DataFrame'idega, aga nüüd sain aru, miks API kasutamine on praktilisem: andmed tulevad otse allikast ja raport ei sõltu enam käsitsi alla laaditud failist.

Sain teada ka seda, et Supabase API võib ühe päringuga tagastada ainult osa andmetest, näiteks 1000 rida. Sellepärast lisasin skripti lehekülgede kaupa laadimise `range(start, end)` abil, et pipeline saaks kätte kõik read, mitte ainult esimesed 1000.

Õppisin ka seda, miks API võtit ei tohi kirjutada otse Python koodi sisse. Hoian Supabase URL-i ja võtme `.env` failis ning `.gitignore` aitab vältida, et need kogemata GitHubi läheksid.

## Mida ma tegin

Ehitasin Week 8 töö jaoks Python skripti, mis töötab ETL pipeline'ina:

- Extract: toon müügi- ja kliendiandmed Supabase Python API kaudu kõikide lehekülgede kaupa.
- Transform: puhastan andmed, arvutan linnade müügiraporti, nädalakokkuvõtte, kuukäibe ja RFM segmendid.
- Validate: kontrollin, et andmed ei ole tühjad ja kogukäive klapib.
- Load: salvestan tulemused CSV raportitena ja Plotly HTML graafikutena.

Pipeline oskab töötada ka näidisandmetega. See on kasulik siis, kui Supabase ühendus ei tööta või kui tahan lihtsalt koodi kiiresti kontrollida.

## Peamised õppimiskohad

Kõige olulisem oli aru saada, et pipeline ei ole lihtsalt üks pikk pandas skript. Pipeline koosneb selgetest sammudest, kus igal osal on oma vastutus. Nii on lihtsam vigu leida, koodi uuesti kasutada ja hiljem automatiseerida.

Sain paremini aru ka funktsioonide mõttest. Näiteks `weekly_sales_report()`, `city_report()` ja `calculate_rfm()` teevad igaüks ühe konkreetse töö. See teeb koodi loetavamaks ja vähendab kordamist.

RFM analüüsis kasutasin jälle Recency, Frequency ja Monetary põhimõtet, aga seekord automatiseeritud kujul. See tähendab, et sama loogikat saab kasutada igal nädalal uute andmetega.

## Tulemused

Päris Supabase API kaudu õnnestus pärast lehekülgede kaupa laadimise lisamist laadida:

- 10118 müügirida tabelist `sales`
- 3150 kliendirida tabelist `customers`
- pärast puhastamist jäi analüüsi 8950 müügirida
- kogukäive oli 2676850.54 EUR
- unikaalseid kliente oli 2540
- RFM analüüs tuvastas 4 segmenti

Kõige suurema kogukulutusega klient oli `customer_id` 3618, kelle `monetary` väärtus oli 27920.86 EUR. Kõige kasumlikum kuu oli 2024-12, käibega 156588.00 EUR.

Linnade järgi oli suurim käive Tallinnas:

- Tallinn: 1006092.81 EUR
- Online: 929622.82 EUR
- Tartu: 472884.31 EUR
- Pärnu: 268250.60 EUR

## Failid

- `week8_api_pipeline.py` - minu Week 8 Python API ja RFM pipeline.
- `Python API ja automatiseeritud RFM pipeline.md` - detailsem töö kirjeldus.
- `output/` - individuaalse pipeline'i loodud CSV ja HTML väljundid.
- `logs/week8_pipeline.log` - logifail, kust on näha individuaalse pipeline'i käivitamise sammud.

## Kuidas käivitada

Supabase API-ga:

```bash
python week-08/individual/week8_api_pipeline.py
```

Näidisandmetega:

```bash
python week-08/individual/week8_api_pipeline.py --sample
```

Koondleht kõigi Week 8 visuaalidega:

```bash
python week-08/individual/combined_visuals.py
```

See loob faili `week-08/individual/combined_visuals.html`, kus tiimitöö, individuaalne töö ja API pipeline'i visuaalid on ühel lehel.

## Minu kokkuvõte

Sain aru, kuidas API, pandas, funktsioonid, logimine ja visualiseerimine kokku üheks andmepipeline'iks ühendada. See on oluline samm edasi, sest sellist lahendust saab hiljem ajastada ja kasutada korduvate raportite tegemiseks ilma käsitsi CSV-faile eksportimata.
## Kuup?evapiirang

Week 8 pipeline kasutab anal??si l?ppkuup?evana `2025-02-28`. API p?ringul seatakse `end_date` v??rtuseks `2025-02-28` ja transform-etapis filtreeritakse ka varu-/n?idisandmed sama kuup?evani.
