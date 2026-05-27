# Nädal 7: Python Pandas

Sel nädalal õppisin kasutama Pythonit ja pandas teeki andmete analüüsimiseks. Varasematel nädalatel töötasin palju SQL-i ja dashboard'idega, aga nüüd sain aru, kuidas samu andmeid saab Pythonis paindlikumalt uurida, puhastada, ühendada, arvutada ja visualiseerida.

Kõigepealt õppisin, mis on pandas DataFrame. Sain aru, et DataFrame sarnaneb SQL-i tabeli või Exceli töölehega, aga Pythonis saab sellega teha rohkem vahepealseid arvutusi ja teisendusi. Harjutasin andmete laadimist ning esmast uurimist käskudega `read_csv()`, `head()`, `info()`, `describe()`, `shape` ja `dtypes`. Need käsud aitasid kiiresti aru saada, mitu rida ja veergu andmestikus on, millised on andmetüübid ning kas andmetes võib olla probleeme.

Teiseks õppisin seostama pandas'e loogikat SQL-iga. Näiteks SQL-i `WHERE` tingimusele vastab pandas'is filtreerimine boolean indexing'u abil, `GROUP BY` loogikale vastab `groupby()` ning SQL-i `JOIN`-ile vastab `merge()`. See aitas mul mõista, et ma ei õpi täiesti uut mõtteviisi nullist, vaid tõlgin juba tuttavat SQL-i loogikat Pythonisse.

Õppisin ka andmeid filtreerima ja grupeerima. Näiteks sain välja võtta ainult Tallinna tellimused, leida suuremad ostud, arvutada käivet linnade kaupa ning võrrelda klientide ostukäitumist. Sain aru, et pandas'is on oluline kasutada õiget süntaksit, eriti mitme tingimusega filtrite puhul, kus tuleb kasutada `&` märki ja panna tingimused sulgudesse.

Kolmandaks õppisin kasutama `merge()` funktsiooni andmete ühendamiseks. See oli tuttav teema SQL-i `JOIN`-ide nädalast, aga pandas'is toimub ühendamine DataFrame'ide vahel. Sain aru, miks `how="left"` on kasulik siis, kui tahan säilitada kõik müügiread ja lisada juurde kliendiinfo ainult siis, kui vastav `customer_id` leidub klienditabelis.

Lisaks õppisin looma uusi arvutatud veerge. Näiteks saab lisada veeru, mis märgib tellimuse suuruse, VIP-staatuse või segmendi. See aitas mul näha, et Python sobib hästi mitmeetapiliseks analüüsiks, kus tulemus ei teki ühe päringuga, vaid samm-sammult andmeid täiendades.

Selle nädala oluline osa oli Plotly Expressiga visualiseerimine. Õppisin looma interaktiivseid tulpdiagramme, joondiagramme, sektordiagramme ja hajuvusdiagramme. Sain aru, et Plotly abil saab Pythonis tehtud analüüsi kohe visuaalselt esitada ning graafikuid saab kasutada nii andmete kontrollimiseks kui ka tulemuste selgitamiseks.

Kõige olulisem praktiline teema oli RFM analüüs. Õppisin, et RFM tähendab `Recency`, `Frequency` ja `Monetary`. Recency näitab, kui hiljuti klient ostis, Frequency näitab ostude arvu ja Monetary näitab kliendi kogukulutust. Nende kolme mõõdiku põhjal saab kliendid jagada segmentidesse, näiteks `VIP Champions`, `Loyal Customers`, `Potential Loyalists`, `At Risk` ja `Lost`.

UrbanStyle'i näite kaudu sain aru, miks RFM analüüs on äriliselt kasulik. See ei näita ainult seda, kui palju müüki toimus, vaid aitab mõista, millised kliendid on kõige väärtuslikumad, kellel on potentsiaali lojaalseks kliendiks saada ja millised kliendid võivad kaduma minna. Sellise info põhjal saab Marko planeerida erinevaid kampaaniaid eri kliendigruppidele.

Kokkuvõttes õppisin sel nädalal:

- laadima andmeid pandas DataFrame'i;
- uurima andmestiku struktuuri ja kvaliteeti;
- kasutama `head()`, `info()`, `describe()`, `shape` ja `dtypes` käske;
- filtreerima andmeid pandas boolean indexing'u abil;
- kasutama `groupby()` funktsiooni andmete koondamiseks;
- sorteerima tulemusi `sort_values()` abil;
- ühendama tabeleid `merge()` funktsiooniga;
- looma uusi arvutatud veerge;
- seostama pandas'e operatsioone SQL-i `WHERE`, `GROUP BY`, `JOIN` ja `ORDER BY` loogikaga;
- looma Plotly Expressiga interaktiivseid graafikuid;
- mõistma RFM analüüsi põhimõtet;
- jagama kliendid segmentidesse nende ostukäitumise põhjal;
- mõtlema, kuidas andmeanalüüs toetab turundus- ja äristrateegiat.

Sel nädalal sain aru, et Python ja pandas annavad analüütikule suurema paindlikkuse kui ainult SQL. SQL sobib väga hästi andmete pärimiseks, aga Python aitab andmeid edasi töödelda, puhastada, arvutada, visualiseerida ja muuta need äriliseks järelduseks. RFM analüüsi kaudu nägin, kuidas müügiridadest saab luua konkreetseid kliendisegmente, mille põhjal saab teha paremaid otsuseid.
