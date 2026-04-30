# Nädal 4: Grupitöö

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
