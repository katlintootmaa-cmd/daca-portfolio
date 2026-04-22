# Nädal 4: SQL agregatsioon

Sel nädalal õppisin, kuidas muuta üksikud andmeread sisukateks kokkuvõteteks, mida saab kasutada päris äriküsimustele vastamiseks. Sain aru, et analüütiku töö ei ole ainult andmete kuvamine, vaid nende koondamine nii, et juhtidel oleks võimalik teha otsuseid selgete numbrite põhjal.

Kõigepealt õppisin kasutama `GROUP BY` lauset ja agregaatfunktsioone nagu `COUNT()`, `SUM()`, `AVG()`, `MIN()` ja `MAX()`. Mõistsin, et `GROUP BY` aitab koondada suuri andmehulkasid väiksemateks loogilisteks gruppideks, näiteks kuude, linnade või kategooriate kaupa. See aitas mul näha, kuidas 1247 müügireast saab teha mõne olulise võtmenäitajaga ülevaate.

Teiseks õppisin vahet tegema `WHERE` ja `HAVING` klauslitel. Sain aru, et `WHERE` filtreerib üksikuid ridu enne grupeerimist, kuid `HAVING` filtreerib juba valmis gruppe pärast agregatsiooni. See eristus aitas mul paremini mõista SQL päringu loogilist tööjärjekorda ja vältida levinud vigu agregaatfunktsioonidega töötamisel.

Kolmandaks õppisin kasutama `CTE`-sid ehk `WITH` klausleid, et jagada keerukad päringud loetavateks vaheetappideks. See tegi päringud palju arusaadavamaks ja näitas, kuidas keerulisemat analüüsi saab sammudeks jagada. Näiteks sain nende abil koostada kliendikokkuvõtteid ja ehitada segmenteerimise loogikat, kus kliendid jagunevad tasemetesse nagu `VIP`, `Aktiivne` ja `Tavaline`.

Lisaks õppisin `window function`-eid, näiteks `ROW_NUMBER()`, `LAG()`, `LEAD()` ja `SUM() OVER (...)`. Sain aru, et need erinevad `GROUP BY`-st selle poolest, et read jäävad alles, kuid iga rea juurde saab lisada uue arvutatud väärtuse. See võimaldas mul vaadata näiteks eelmise kuu käivet, leida kategooriate TOP-tooteid ja mõista paremini erinevust `GROUP BY` ja `PARTITION BY` vahel.

Selle nädala jooksul õppisin siduma SQL-i tehnilised võtted äriloogikaga. Harjutused näitasid, kuidas vastata küsimustele nagu:

- kuidas müük kuude lõikes muutub;
- millised linnad või kategooriad toovad suurima käibe;
- kes on kõige väärtuslikumad kliendid;
- kuidas leida andmetest varude või müügi mittevastavusi.

Kokkuvõttes õppisin sel nädalal:

- kasutama `GROUP BY` lauset andmete grupeerimiseks;
- rakendama agregaatfunktsioone kokkuvõtlike näitajate arvutamiseks;
- eristama `WHERE` ja `HAVING` kasutuskohti;
- kirjutama loetavamaid päringuid `CTE`-de abil;
- kasutama `window function`-eid trendide, järjestuste ja võrdluste leidmiseks;
- mõtlema rohkem äriküsimuse kui ainult SQL süntaksi peale.

Sel nädalal sain aru, et SQL agregatsioon on üks olulisemaid oskusi andmeanalüüsis, sest just selle abil saab toorandmetest teha arusaadavaid kokkuvõtteid, mustreid märgata ja esitada tulemusi nii, et neist oleks päriselt kasu.
