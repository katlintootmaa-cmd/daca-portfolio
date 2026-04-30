# Nädal 4: Iseseisev töö

## Mida tegin

Selle nädala iseseisva töö käigus õppisin SQL agregatsiooni ja harjutasin, kuidas muuta üksikud andmeread kokkuvõtlikeks näitajateks. Fookuses olid `GROUP BY`, `HAVING`, `CTE` ja `window function`-id ning nende kasutamine UrbanStyle'i müügi-, kliendi- ja inventuuriandmete analüüsimisel.

## Tegevused

- Kontrollisin, et `Supabase SQL Editor` töötab ja UrbanStyle'i andmebaasile on ligipääs olemas.
- Lisasin `NotebookLM`-i selle nädala RAG-failid:
  - `4_0_R1_sql_aggregation_concepts-rag.md`
  - `4_0_R2_sql_aggregation_urbanstyle_application-rag.md`
- Harjutasin `GROUP BY` kasutamist, et koondada müüki kuude, linnade ja kategooriate lõikes.
- Kasutasin agregaatfunktsioone `COUNT()`, `SUM()`, `AVG()`, `MIN()` ja `MAX()`, et arvutada peamisi ärinäitajaid.
- Õppisin eristama `WHERE` ja `HAVING` klauslite rolli ning filtreerima õigel hetkel.
- Kirjutasin `CTE`-dega loetavamaid SQL päringuid, et jagada keerukam analüüs sammudeks.
- Katsetasin `window function`-eid, nagu `LAG()`, `ROW_NUMBER()` ja `SUM() OVER (...)`, et võrrelda perioode ja järjestada tulemusi.
- Rakendasin neid oskusi inventuuristatistika ülesandes, kus võrdlesin toodete müüki, laoseisu ja kategooriate kasumlikkust.
- Koostasin tulemuste põhjal lühikese ärilise tõlgenduse ja visualiseerisin kategooriate võrdluse diagrammina.

## Õpitud teemad

- `GROUP BY` aitab koondada toorandmed loogilisteks gruppideks, näiteks kuu või kategooria järgi.
- `HAVING` sobib siis, kui tahame filtreerida juba agregatsiooniga loodud gruppe.
- `CTE` muudab keerukad päringud selgemaks ja lihtsamini loetavaks.
- `window function`-id erinevad `GROUP BY`-st selle poolest, et read jäävad alles, kuid neile lisatakse uus arvutatud väärtus.
- SQL analüüs muutub kasulikuks siis, kui tulemused seotakse äriküsimuste ja otsustega.

## Kokkuvõte

Iseseisva töö lõpuks oskan paremini kasutada SQL agregatsiooni, et leida müügitrende, võrrelda kliendigruppe ja hinnata inventuuri seisu. See nädal aitas mul mõista, kuidas koostada päringuid, mis ei näita ainult andmeid, vaid annavad ka selge aluse äriliste soovituste tegemiseks.
