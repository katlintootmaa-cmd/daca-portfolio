# Nädal 4: Grupitöö

English version: [README_EN.md](README_EN.md)

## Rollijaotus

| Roll | Tiimiliige | Ülesanne |
|------|------------|----------|
| A | Karmo | Müügi koondandmed: arvutas müügi KPI-d, perioodide võrdlused ja peamised tulumustrid. |
| B | Mari | Kliendigruppide analüüs: koondas kliendid segmentide, linnade või ostukäitumise järgi. |
| C | Kätlin | Inventuuristatistika: analüüsis laoseisu, toodete saadavust ja varude riske. |
| D | Ragnar | Turunduskampaaniate ROI: hindas kampaaniate mõju müügile ja klientide aktiivsusele. |

## Rollide kirjeldused

- Roll A ehk müügi koondandmete analüütik vastutas juhtkonnale sobivate müügi KPI-de eest. Roll arvutas käibe, tellimuste arvu, keskmise ostu ja perioodide võrdlused.
- Roll B ehk kliendigruppide analüütik vastutas klientide koondvaate eest. Roll leidis kliendisegmendid, aktiivsemad kliendid ja grupid, millele turundus või müük peaks tähelepanu pöörama.
- Roll C ehk inventuuristatistika analüütik vastutas laoseisu ja tootevarude koondpildi eest. Roll hindas, millised kategooriad või tooted vajavad varude juhtimisel suuremat tähelepanu.
- Roll D ehk turunduse ROI analüütik vastutas kampaaniate tulemuslikkuse mõõtmise eest. Roll võrdles kampaaniate mõju müügile, klientide aktiivsusele ja kanalite tasuvusele.

## Mida tegime

Selle nädala grupitöö käigus rakendasime SQL agregatsiooni UrbanStyle'i äriprobleemi lahendamiseks. Eesmärk oli koostada Kristile juhatuse koosoleku jaoks koondraportid, mis annavad kiire ülevaate müügist, kliendigruppidest, inventuurist ja turunduse tulemuslikkusest.

## Grupitöö fookus

Töötasime tabelitega `sales`, `customers`, `products`, `inventory` ja võimalusel ka `web_logs`. Kasutasime sessioonis õpitud võtteid, nagu `GROUP BY`, `HAVING`, `CTE` ja `window function`-id, et muuta toorandmed äriliselt tõlgendatavateks kokkuvõteteks.

## Rollid ja ülesanded

- Roll A: müügi koondandmed kuude ja kategooriate lõikes, et leida käibetrendid, tellimuste arv ja keskmine tellimusväärtus.
- Roll B: kliendigruppide analüüs, et segmenteerida kliendid `VIP`, `Regular` ja `Uus` rühmadesse ning leida TOP-kliendid.
- Roll C: inventuuristatistika, et võrrelda laoseisu, müüki ja brutokasumit kategooriate ning toodete lõikes.
- Roll D: turunduskampaaniate ROI, et hinnata kanalite ja allikate tulemuslikkust ning tuvastada mõõtmise kitsaskohad.

## Tööprotsess

- Lugesime läbi Anna Metsa väljakutse ja sõnastasime, milliseid koondnumbreid Kristi juhatusele vajab.
- Jagasime meeskonnas rollid domeenide kaupa laiali.
- Iga osaleja koostas oma alaülesande põhjal SQL päringud ja lühikese ärilise kokkuvõtte.
- Kontrollisime, et päringutes oleks kasutatud vähemalt `GROUP BY`, vajadusel `HAVING` ja keerukamates lahendustes ka `CTE` või `window function`-eid.
- Esitlesime oma leiud üksteisele ja koondasime peamised järeldused ühiseks väljundiks.

## Kasutatud SQL oskused

- `GROUP BY`
- `HAVING`
- `COUNT`
- `SUM`
- `AVG`
- `MIN` ja `MAX`
- `CASE WHEN`
- `CTE` ehk `WITH`
- `LAG()` ja teised `window function`-id
- tabelite ühendamine `JOIN` abil

## Peamised õppetunnid

- Agregatsioon aitab muuta suure hulga üksikuid ridu juhtkonnale arusaadavateks võtmenäitajateks.
- `HAVING` on vajalik siis, kui tahame filtreerida juba kokku võetud gruppe, mitte üksikuid ridu.
- `CTE` muudab keerukamad päringud loetavamaks ja aitab analüüsi sammudeks jagada.
- Äriline väärtus tekib siis, kui numbrite juurde lisada ka tõlgendus ja soovitus.
- Turundusanalüüs sõltub tugevalt andmete kvaliteedist; kui kõik kanalid ei ole korrektselt mõõdetud, jääb osa pildist puudulikuks.

## Kokkuvõte

Grupitöö tulemusena koostasime UrbanStyle'i jaoks koondvaate, mis seob müügitrendid, kliendisegmendid, laoseisu ja turunduse mõju ühtseks äriloogikaks. Õppisime, kuidas `GROUP BY`, `HAVING`, `CTE` ja `window function`-id aitavad vastata CEO tasemel küsimustele ning kuidas erinevate rollide tulemused üheks selgeks raportiks kokku tuua.
