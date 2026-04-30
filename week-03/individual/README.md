# Nädal 3: Iseseisev töö

## Mida tegin

Selle nädala iseseisva töö käigus õppisin SQL JOIN-e ja harjutasin, kuidas ühendada eri tabelites olevad andmed üheks tervikvaateks. Fookuses olid UrbanStyle'i andmebaasi tabelid `sales`, `customers` ja `products`.

## Tegevused

- Kontrollisin, et Supabase SQL Editor töötab ja UrbanStyle'i andmebaasile on ligipääs olemas.
- Lisasin NotebookLM-i selle nädala RAG-failid:
  - `3_0_R1_sql_joins_concepts-rag.md`
  - `3_0_R2_sql_joins_urbanstyle_application-rag.md`
- Kordasin, kuidas tabelid omavahel seotud on primary key ja foreign key veergude kaudu.
- Harjutasin `INNER JOIN`-i, et ühendada ainult need read, millel on mõlemas tabelis sobiv vaste.
- Harjutasin `LEFT JOIN`-i, et säilitada kõik vasaku tabeli read ja leida ka puuduvad seosed.
- Kasutasin `LEFT JOIN + WHERE IS NULL` mustrit, et leida kliente, kes on registreerunud, aga pole kunagi ostnud.
- Koostasin päringuid müümata toodete leidmiseks.
- Harjutasin mitme tabeli ühendamist, et näha ühes vaates kliendi nime, müügi kuupäeva, toote nime, kategooriat, kogust ja müügisummat.
- Kasutasin tabeli aliaseid, näiteks `s`, `c` ja `p`, et päringud oleksid lühemad ja loetavamad.
- Koostasin Anna turundusvajaduste põhjal päringuid, mis aitavad leida parimaid kliente, populaarseid tootekategooriaid ja linnade kaupa müügitulemusi.

## Õpitud teemad

- `INNER JOIN` näitab ainult kattuvaid andmeid.
- `LEFT JOIN` näitab kõik vasaku tabeli read ja lisab parema tabeli andmed siis, kui vaste on olemas.
- `WHERE ... IS NULL` aitab leida puuduvaid seoseid, näiteks ostuta kliente või müümata tooteid.
- Mitme tabeli ühendamine aitab vastata päris äriküsimustele, sest vajalik info on tihti jagatud mitme tabeli vahel.
- Tabeli aliased muudavad SQL päringud selgemaks ja lihtsamini loetavaks.

## Kokkuvõte

Iseseisva töö lõpuks oskan paremini ühendada `sales`, `customers` ja `products` tabeleid ning koostada päringuid, mis muudavad eraldi tabelites olevad andmed arusaadavaks raportiks. See aitab vastata küsimustele nagu kes on parimad kliendid, mida nad ostavad, millised tooted ei müü ja millistes linnades on erinevad tootekategooriad populaarsemad.
