# Nädal 8: mida ma õppisin

Selle nädala jooksul õppisin, kuidas muuta varasem RFM analüüs automatiseeritud Python pipeline'iks. Kui varem töötasin rohkem CSV failidega, siis nüüd sain andmeid küsida otse Supabase API kaudu. Sain aru, miks API kasutamine on praktiline: raport saab võtta värsked andmed otse allikast ja ma ei pea faile käsitsi eksportima.

Õppisin ka seda, et API päringud vajavad korralikku struktuuri. Supabase tagastab ühe päringuga piiratud hulga ridu, seega lisasin andmete laadimise lehekülgede kaupa. See aitas kätte saada kogu vajaliku müügi- ja kliendiandmestiku, mitte ainult esimesed read.

Pipeline'i ehitades sain paremini aru ETL loogikast:

- Extract: toon andmed API kaudu või kasutan vajadusel näidisandmeid.
- Transform: puhastan andmed, ühendan tabelid ja arvutan raportid.
- Validate: kontrollin, et andmed ja kogusummad oleksid loogilised.
- Load: salvestan tulemused CSV ja HTML raportitena.

Minu jaoks oli oluline õppimiskoht ka see, et API võtmeid ei tohi kirjutada otse Python koodi sisse. Hoidsin Supabase URL-i ja võtme `.env` failis ning sain aru, miks `.gitignore` on selliste tundlike andmete kaitsmiseks vajalik.

RFM analüüsi juures kordasin Recency, Frequency ja Monetary põhimõtet, aga seekord tegin selle automatiseeritult. See tähendab, et sama loogikat saab kasutada uuesti iga kord, kui andmed uuenevad.

Visuaalide poolel õppisin kasutama Plotly graafikuid ja salvestama tulemusi HTML failidena. Nii saab pipeline'i väljundeid lihtsamalt avada, jagada ja võrrelda.

Kokkuvõttes sain aru, kuidas Python, pandas, Supabase API, logimine, valideerimine ja visualiseerimine töötavad koos üheks korratavaks andmepipeline'iks. See nädal näitas mulle, kuidas käsitsi tehtud analüüsist saab tööriist, mida saab käivitada uuesti ja hiljem ka automatiseerida.

## Failistruktuur

- `individual/` - minu individuaalse töö failid, pipeline'i demo ja visuaalide eksport.
- `team/` - tiimitöö modulaarne pipeline.
- `individual/week8_individual_summary.md` - detailsem individuaalse töö kirjeldus.
- `individual/Python API ja automatiseeritud RFM pipeline.md` - põhjalikum API pipeline'i selgitus.
