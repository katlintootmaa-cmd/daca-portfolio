# Nädal 1: SQL Basics

Sel nädalal õppisin SQL-i põhikäske ja harjutasin andmete lugemist, filtreerimist ning loendamist UrbanStyle'i andmebaasi näitel. Fookuses oli arusaamine, kuidas päringutega andmeid uurida ilma algandmeid muutmata.

## Mida õppisin

- `SELECT` ja `FROM` abil sain valida vajalikud veerud ja määrata, millisest tabelist andmeid võtta
- `ORDER BY` ja `LIMIT` abil õppisin tulemusi sorteerima ja piirama
- `WHERE` klausliga õppisin andmeid filtreerima erinevate tingimuste järgi
- kasutasin võrdlusoperaatoreid nagu `=`, `>`, `<`, `>=`, `<=`
- õppisin kasutama loogikaoperaatoreid `AND` ja `OR`
- sain aru, kuidas töötavad `BETWEEN`, `IN`, `LIKE` ja `IS NULL`
- `DISTINCT` abil õppisin leidma unikaalseid väärtusi
- `COUNT(*)`, `COUNT(veerg)` ja `COUNT(DISTINCT veerg)` abil õppisin ridu ja unikaalseid väärtusi loendama

## Mida praktikas tegin

- vaatasin `sales`, `customers` ja `products` tabelite sisu
- otsisin suurimaid ja väikseimaid müüke
- filtreerisin andmeid kuupäeva, summa ja kanali järgi
- otsisin ridu, kus `customer_id` puudus
- kontrollisin, kas tabelites on duplikaate
- võrdlesin kõigi ridade arvu ja unikaalsete `sale_id` väärtuste arvu
- harjutasin andmekvaliteedi probleemide märkamist, näiteks `NULL` väärtused ja võimalikud duplikaadid

## Olulisemad taipamised

- `SELECT *` ei ole hea praktika, kui eesmärk on töötada selgelt ja efektiivselt
- `NULL` ei ole sama mis `0` või tühi väärtus, seega tuleb selle leidmiseks kasutada `IS NULL`
- `COUNT(*)` ja `COUNT(veerg)` annavad erineva tulemuse, kui andmetes on puuduvaid väärtusi
- SQL aitab väga kiiresti leida mustreid ja andmeprobleeme, kui küsimus on õigesti sõnastatud

## Kokkuvõte

Nädal 1 andis mulle tugeva aluse SQL-i kasutamiseks. Õppisin kirjutama lihtsaid, kuid praktilisi päringuid, millega saab andmeid uurida, filtreerida ja kontrollida. Järgmiseks tahan muutuda kindlamaks keerukamate päringute kirjutamisel ja õppida oma SQL-i paremini dokumenteerima.
