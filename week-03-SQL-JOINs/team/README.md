# Nädal 3: Grupitöö

English version: [README_EN.md](README_EN.md)

## Mida tegime

Selle nädala grupitöö käigus rakendasime SQL JOIN-e UrbanStyle'i äriprobleemi lahendamiseks. Eesmärk oli aidata Annal ja Toomasel saada vastuseid küsimustele, mis nõuavad mitme tabeli ühendamist: kes ostab, kes ei osta, millised tooted müüvad, millised tooted ei müü ja millised müügikanalid töötavad kõige paremini.

## Grupitöö fookus

Töötasime tabelitega `sales`, `customers`, `products` ja vajadusel ka inventuuriandmetega. Kasutasime sessioonis õpitud JOIN-tüüpe, et koostada praktilisi päringuid ja tõlgendada tulemusi ärilises kontekstis.

## Rollid ja ülesanded

- Roll A: Mari vastutas müügi ja klientide ühendamise eest `INNER JOIN` abil.
- Roll B: Kätlin leidis kliendid, kes on registreerunud, aga pole ostnud, kasutades `LEFT JOIN + WHERE IS NULL` mustrit.
- Roll C: Ragnar analüüsis tooteid ja inventuuri `LEFT JOIN` loogikaga, et leida müümata või riskiga tooted.
- Roll D: Karmo võrdles turunduse ja müügi seoseid `INNER JOIN` abil ning tõlgendas kanalite mõju.
- Müügi ja klientide ühendamine `INNER JOIN` abil, et leida ostnud kliendid ja TOP kliendid kogumüügi järgi.
- Klientide leidmine, kes on registreerunud, aga pole kunagi ostnud, kasutades `LEFT JOIN + WHERE IS NULL` mustrit.
- Müümata toodete leidmine `LEFT JOIN` abil ning inventuuriandmete analüüsimine.
- Müügikanalite võrdlemine, et aru saada, millised kanalid toovad enim müüki ja kliente.
- Mitme tabeli ühendamine, et näha koos kliendi, müügi ja toote infot.
- Puuduvate seoste analüüs ehk anti-JOIN loogika kasutamine klientide ja toodete puhul.

## Rollide kirjeldused

- Roll A ehk müügi ja klientide ühendaja vastutas ostnud klientide vaate eest. Rolli eesmärk oli näidata, millised kliendid tekitavad müüki ja kuidas `INNER JOIN` aitab luua kliendipõhise müügipildi.
- Roll B ehk ostuta klientide analüütik vastutas puuduvate ostuseoste leidmise eest. Roll kasutas `LEFT JOIN` ja `WHERE IS NULL` loogikat, et tuvastada kliendid, kellel on konto, aga puudub ostuajalugu.
- Roll C ehk toodete ja inventuuri analüütik vastutas müümata või riskiga toodete tuvastamise eest. Roll ühendas toote- ja inventuuriandmeid, et hinnata, kus tekib laoseisu või müügipotentsiaali probleem.
- Roll D ehk turunduse ja müügi ühendaja vastutas kanalite mõju analüüsi eest. Roll sidus turunduse või müügikanalite info müügitulemustega ja tõlgendas, millised kanalid toovad ärilist väärtust.

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
