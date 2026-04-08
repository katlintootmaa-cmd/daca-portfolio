# Nädal 2: SQL Cleaning
# Kokkuvõte: mida ma õppisin

Sel nädalal õppisin SQL-is andmete puhastamist ja sain aru, et enne analüüsi tegemist peab andmete kvaliteedi alati üle kontrollima. Õppisin, et vigased või segased andmed võivad anda täiesti valesid järeldusi ning seepärast ei tohi andmeid kohe muuta, vaid kõigepealt tuleb probleemid tuvastada, dokumenteerida, testida ja alles siis parandada.

Kõigepealt õppisin duplikaatide leidmist. Sain aru, kuidas kasutada `GROUP BY` ja `HAVING` tingimust, et leida väärtused, mis korduvad rohkem kui üks kord. Lisaks õppisin kasutama `ROW_NUMBER()` funktsiooni, et nummerdada sama grupi read ja eristada originaalkirjet duplikaatidest. See aitas mul mõista, kuidas otsustada, milline rida alles jätta ja milline on üleliigne koopia.

Teiseks õppisin paremini mõistma `NULL` väärtusi. Sain selgeks, et `NULL`, tühi string (`''`) ja number `0` ei tähenda SQL-is sama asja. Õppisin kasutama tingimusi `IS NULL` ja `IS NOT NULL`, et leida puuduvaid andmeid, ning funktsiooni `COALESCE()`, et kuvada puuduvate väärtuste asemel arusaadav vaikeväärtus. Lisaks sain aru, et `NULL` väärtusi ei tohi kontrollida kujul `= NULL`, sest see ei tööta õigesti.

Kolmandaks õppisin andmevormingute ühtlustamist. Harjutasin teksti puhastamist funktsioonidega `TRIM()`, `UPPER()`, `LOWER()` ja `INITCAP()`, et eemaldada liigsed tühikud ja muuta kirjapilt ühtlaseks. Samuti õppisin kuupäevade vormindamist ja teisendamist, kasutades kuupäevafunktsioone ning `TO_CHAR()` ja `CAST()`-i. See aitas mõista, miks sama tähendusega väärtused võivad andmebaasis olla eri kujul ja miks need tuleb enne analüüsi ühtlustada.

Sain ka aru, et andmete puhastamine ei tähenda ainult SQL päringute kirjutamist, vaid ka andmete kvaliteedi kontrollimist erinevates tabelites. Grupitöö juhendi põhjal õppisin vaatama andmeid domeenide kaupa: müügiandmed, kliendiandmed, tooteandmed ja ristvalideerimine tabelite vahel. See õpetas mind kontrollima, kas müük viitab olemasolevale kliendile ja tootele ning kas hinnad ja kogused omavahel klapivad.

Oluline õppetund oli ka ohutu tööviis. Õppisin, et andmete puhastamist tuleb teha testkoopial, mitte production tabelis. Enne muudatuste tegemist tuleb kokku lugeda probleemid, kirjeldada need raportis ja alles seejärel teha parandused. See aitas mul mõista, et andmeanalüütiku töö ei ole ainult tulemuse saamine, vaid ka korrektse ja usaldusväärse protsessi järgimine.

Dokumentidest jäi hästi meelde, kui suur mõju võib vigastel andmetel olla. Näiteks müügitabelis leiti tuhandeid duplikaate, puuduvad `customer_id` väärtused ja isegi tuleviku kuupäevad. See näitas mulle praktiliselt, kuidas halva kvaliteediga andmed võivad moonutada müügiaruandeid ja viia valede äriotsusteni.

Kokkuvõttes õppisin sel nädalal:

- leidma duplikaate `GROUP BY`, `HAVING` ja `ROW_NUMBER()` abil;
- tuvastama ja käsitlema puuduvaid väärtusi `IS NULL`, `IS NOT NULL`, `COALESCE()` ja `NULLIF()` abil;
- puhastama ja ühtlustama tekstivälju ning kuupäevi;
- töötama turvaliselt testkoopiaga enne pärisandmete muutmist;
- koostama puhastamisraportit, kus SQL tulemus tuleb tõlkida ka ärilise tähendusega järeldusteks.

Sel nädalal sain aru, et puhtad andmed on usaldusväärse analüüsi alus. Kui andmeid ei kontrollita ega puhastata, siis ei saa ka raportite ega otsuste kvaliteeti usaldada.
