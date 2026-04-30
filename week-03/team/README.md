# Nädal 3: Grupitöö

## Mida tegime

Selle nädala grupitöö käigus rakendasime SQL JOIN-e UrbanStyle'i äriprobleemi lahendamiseks. Eesmärk oli aidata Annal ja Toomasel saada vastuseid küsimustele, mis nõuavad mitme tabeli ühendamist: kes ostab, kes ei osta, millised tooted müüvad, millised tooted ei müü ja millised müügikanalid töötavad kõige paremini.

## Grupitöö fookus

Töötasime tabelitega `sales`, `customers`, `products` ja vajadusel ka inventuuriandmetega. Kasutasime sessioonis õpitud JOIN-tüüpe, et koostada praktilisi päringuid ja tõlgendada tulemusi ärilises kontekstis.

## Rollid ja ülesanded

- Müügi ja klientide ühendamine `INNER JOIN` abil, et leida ostnud kliendid ja TOP kliendid kogumüügi järgi.
- Klientide leidmine, kes on registreerunud, aga pole kunagi ostnud, kasutades `LEFT JOIN + WHERE IS NULL` mustrit.
- Müümata toodete leidmine `LEFT JOIN` abil ning inventuuriandmete analüüsimine.
- Müügikanalite võrdlemine, et aru saada, millised kanalid toovad enim müüki ja kliente.
- Mitme tabeli ühendamine, et näha koos kliendi, müügi ja toote infot.
- Puuduvate seoste analüüs ehk anti-JOIN loogika kasutamine klientide ja toodete puhul.

## Tööprotsess

- Lugesime läbi Anna ja Toomase väljakutse.
- Jagasime rollid ja alaülesanded meeskonnaliikmete vahel.
- Iga osaleja koostas oma rolli põhjal SQL päringud.
- Kontrollisime, kas päringud töötavad ja kas JOIN-tingimused on õiged.
- Jagasime tulemusi meeskonnas ja tõlgendasime neid Anna jaoks arusaadavalt.
- Koondasime peamised leiud, üllatused, soovitused ja puuduvad andmed ühisesse väljundisse.

## Kasutatud SQL oskused

- `INNER JOIN`
- `LEFT JOIN`
- `LEFT JOIN + WHERE IS NULL`
- mitme tabeli ühendamine
- `GROUP BY`
- `ORDER BY`
- `COUNT`
- `SUM`
- tabeli aliased
- äriküsimuse tõlkimine SQL päringuks

## Peamised õppetunnid

- JOIN-id aitavad ühendada eri tabelites olevad andmed üheks tervikpildiks.
- `INNER JOIN` sobib siis, kui tahame näha ainult olemasolevaid vasteid, näiteks ostnud kliente.
- `LEFT JOIN + WHERE IS NULL` sobib puuduvate seoste leidmiseks, näiteks ostuta klientide või müümata toodete tuvastamiseks.
- Mitme tabeli JOIN aitab vastata keerukamatele äriküsimustele, näiteks millised tootekategooriad müüvad millistes kanalites või linnades kõige paremini.
- SQL päringu tulemusest üksi ei piisa; oluline on lisada ka äriline tõlgendus ja soovitus.

## Kokkuvõte

Grupitöö tulemusena harjutasime SQL JOIN-ide kasutamist reaalse UrbanStyle'i äriprobleemi lahendamiseks. Õppisime jagama analüüsi väiksemateks rollipõhisteks ülesanneteks, koostama JOIN-päringuid ning koondama tulemused Anna jaoks arusaadavaks soovituseks. See töö valmistab ette järgmise nädala teemat, kus JOIN-idele lisanduvad koondarvutused, `GROUP BY`, `HAVING`, CTE-d ja window functions.
