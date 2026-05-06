# GT_Viz_andmed grupitöö: Power BI samm-sammult juhend

Versioon: Microsoft Power BI Desktop 2.153.910.0 64-bit, April 2026  
Töö: DACA nädal 6, visualiseerimise andmed, grupitöö  
Andmeallikas: UrbanStyle andmed Power BI failis või Supabase/Postgres andmebaasis

## 1. Eesmärk

Selle juhendi eesmärk on viimistleda eelmise nädala UrbanStyle dashboard nii, et see ei oleks ainult graafikute kogum, vaid jutustaks selge andmeloo.

Nädal 6 grupitöös teeb iga meeskonnaliige ühe asukoha vaate:

| Roll | Vaade | Fookus |
|---|---|---|
| A | Tallinn | Suurim kauplus, tugevused ja kasvuvõimalused |
| B | Tartu | Teine kauplus, võimalik langustrend ja põhjused |
| C | Pärnu | Väiksem kauplus, hooajalisus ja suveperioodi mõju |
| D | E-pood | Online-kanal, kasvutempo ja digitaalse kanali potentsiaal |

Iga osaleja loob ühe dashboard'i, lisab sellele juhtide kokkuvõtte, annotatsioonid, viitejoone ja lühikese andmeloo. Meeskond paneb tulemused kokku üheks koondlooks.

Miinimumtulemus iga inimese kohta:

- 1 asukohapõhine dashboard;
- 3-5 visuali;
- 3-5 järeldusega juhtide kokkuvõte;
- vähemalt 2 annotatsiooni;
- vähemalt 1 viitejoon;
- 3-4-lauseline andmelugu;
- ekraanipilt või link portfoolio jaoks.

### 1.1. Töö üldine järjekord

Selle töö tegemisel tuleb läbida mitu väiksemat etappi:

- Power BI nädala 6 faili loomine eelmise nädala dashboard'i põhjal;
- rollipõhise vaate tegemine, eriti Tallinna ja Tartu dashboard'i jaoks;
- KPI kaartide, müügitrendi ja TOP 5 visualide korrastamine;
- annotatsioonide, viitejoone ja juhtide kokkuvõtte lisamine;
- 3-4-lauselise andmeloo kirjutamine;
- meeskonna koondloo ja alarühmade kokkuvõtte sõnastamine;
- portfoolio README teksti täiendamine;
- AI kasutamise kirjeldamine nii, et oleks selge, mida AI aitas teha ja mida kontrolliti ise.

Tee need sammud sellises järjekorras.

1. Ava eelmise nädala Power BI fail ja salvesta sellest nädala 6 koopia.
2. Loo uus raportileht oma rolli jaoks: `Tallinn`, `Tartu`, `Parnu` või `E-pood`.
3. Pane lehele õige page-level filter:
   - Tallinna puhul `sales[store_location] = Tallinn`;
   - Tartu puhul `sales[store_location] = Tartu`;
   - Pärnu puhul `sales[store_location] = Pärnu`;
   - e-poe puhul `sales[channel] = online`.
4. Kontrolli, et põhimeasure'id oleksid olemas: `Kogukäive`, `Tellimusi`, `Kliente`, `Keskmine tellimus` ja `Müüdud ühikuid`.
5. Lisa 3-4 KPI kaarti, et juht näeks kohe müügi, tellimuste, klientide ja keskmise tellimuse seisu.
6. Lisa joondiagramm müügitrendi jaoks ja kasuta X-teljel kuupäeva või `Date[YearMonth]` välja.
7. Lisa TOP 5 toodete või kategooriate tulpdiagramm, sorteeri see kahanevalt ja rakenda `Top N = 5` filter.
8. Lisa vähemalt üks rollipõhine lisavisual:
   - Tallinn: kanalite või kategooriate võrdlus;
   - Tartu: tugevamate ja nõrgemate kategooriate võrdlus;
   - Pärnu: hooajalisus kuude lõikes;
   - e-pood: online-kanali kasv või toodete võrdlus.
9. Lisa viitejoon müügitrendi visualile, näiteks keskmine kuukäive, eesmärk või teise asukoha võrdluspunkt.
10. Lisa vähemalt kaks annotatsiooni, mis ei ütle ainult numbrit, vaid selgitavad selle tähendust. Hea annotatsioon vastab küsimusele: "Ja mis siis?"
11. Kirjuta juhtide kokkuvõte 3-5 lühikese järeldusena: mis toimub, miks see on oluline ja mida Anna peaks tegema.
12. Kirjuta 3-4-lauseline andmelugu vormis: olukord, peamine fakt, äriline tõlgendus ja soovitus.
13. Salvesta dashboard'ist ekraanipilt nädala 6 kausta.
14. Lisa portfooliosse ekraanipilt, oma roll, juhtide kokkuvõte, andmelugu, meeskonna koondvaade ja AI kasutamise kirjeldus.
15. Meeskonna töö jaoks koonda iga roll üheks lühikeseks looks: Tallinn kui tugev põhikauplus, Tartu kui tähelepanu vajav kauplus, Pärnu kui hooajaline kauplus ja e-pood kui skaleeritav kasvukanal.

Kui kasutad AI abi, kirjuta portfooliosse näiteks nii:

```text
Kasutasin AI-d Power BI dashboard'i andmeloo, annotatsioonide ja juhtide kokkuvõtte sõnastamiseks. Kontrollisin Power BI visualide põhjal üle, et AI ei lisaks numbreid ega põhjuseid, mida andmetes ei olnud.
```

### 1.2. Pealkirjad ja vormistus Power BI-s

Kasuta seda osa siis, kui visualid on sisuliselt olemas, aga pealkirjad, tekstikastid või kujundus vajavad veel korrastamist.

#### Kuidas muuta visuali pealkirja

1. Klõpsa visuali peal, mille pealkirja tahad muuta.
2. Paremal ava `Format visual`.
3. Ava jaotis `General`.
4. Ava `Title`.
5. Kontrolli, et `Title` oleks sisse lülitatud.
6. Kirjuta väljale `Text` uus pealkiri.
7. Pane pealkiri lühikeseks ja sisukaks, näiteks:
   - `Müügikäibe trend kuude lõikes`;
   - `TOP 5 tooted kogukäibe järgi`;
   - `Käive kategooriate lõikes`;
   - `Kliendisegmendid käibe järgi`.

Hea pealkiri ütleb, mida visual näitab. Väldi liiga üldist pealkirja nagu `Chart`, `Sum of total_price` või `Visual 1`.

#### Kuidas pealkiri eemaldada

1. Klõpsa visuali peal.
2. Ava paremal `Format visual`.
3. Ava `General` > `Title`.
4. Lülita `Title` välja.

Eemalda visuali enda pealkiri siis, kui kasutad selle kohal eraldi tekstikasti pealkirjana. Ära jäta korraga alles nii tekstikasti pealkirja kui ka visuali automaatset pealkirja, sest siis tekib topeltpealkiri.

#### Kuidas muuta KPI kaardi nime

KPI kaardil võib Power BI näidata mõõdiku tehnilist nime, näiteks `Sum of total_price`. Selle parandamiseks on kaks võimalust.

Variant A: muuda visuali pealkirja.

1. Klõpsa KPI kaardil.
2. Ava `Format visual`.
3. Ava `General` > `Title`.
4. Lülita `Title` sisse.
5. Kirjuta pealkirjaks näiteks `Kogukäive`, `Müüke`, `Kliente` või `Keskmine ost`.

Variant B: muuda väljanime ainult selles visualis.

1. Klõpsa KPI kaardil.
2. Paremal väljade alas leia kasutatud mõõdik.
3. Ava mõõdiku kõrval rippmenüü.
4. Vali `Rename for this visual`.
5. Kirjuta kasutajasõbralik nimi.

Füüsilise poe dashboard'il kõlab `Müüke` või `Oste` sageli loomulikumalt kui `Tellimusi`. E-poe puhul sobib `Tellimusi` hästi.

#### Kuidas tekstikasti muuta või kustutada

Tekstikastid on kasulikud pealkirjade, annotatsioonide ja andmeloo jaoks.

1. Klõpsa tekstikasti serval, mitte ainult teksti sees.
2. Kui tahad teksti muuta, tee tekstikasti sees topeltklõps ja kirjuta uus tekst.
3. Kui tahad tekstikasti liigutada, lohista seda servast.
4. Kui tahad tekstikasti kustutada, vali tekstikast ja vajuta `Delete`.
5. Kui kustutamine ei tööta, kontrolli, et valitud oleks kogu tekstikast, mitte ainult tekstikursor selle sees.

Kui tekstikast katab visuali või jääb graafiku peale segama, liiguta see visuali kõrvale või tee väiksemaks. Annotatsioon peab toetama visuali, mitte selle andmeid kinni katma.

#### Ühtne vormistus kogu dashboard'il

Kui dashboard näeb liiga kirju välja, tee need parandused:

1. Kasuta kogu lehel sama fonti, näiteks `Segoe UI`.
2. Kasuta pealkirjades tumedat teksti: `#1E2430`.
3. Kasuta selgitavas tekstis halli: `#7A858E`.
4. Kasuta positiivse või olulise rõhutuse jaoks türkiisi: `#18AFA5`.
5. Kasuta negatiivse koha rõhutamiseks crimson punast: `#DC143C`.
6. Pane lehe taust väga heledaks: `#F8FAFA` või `#F6F7F8`.
7. Pane KPI kaartide ja tekstiplokkide taustaks helehall või hele mint: `#F1F3F4`, `#EEF1F2` või `#E3F5F3`.
8. Ära kasuta igal visualil erinevat värvi. Piisab ühest põhivärvist ja ühest hoiatusvärvist.
9. Joonda KPI kaardid ühele reale ja jäta nende vahele sama suur vahe.
10. Jäta visualide ümber tühja ruumi, et leht ei näeks ülerahvastatud välja.

Soovituslik suuruste loogika:

| Element | Soovitus |
|---|---|
| Dashboard'i põhipealkiri | `22-26 pt`, tume |
| Visuali pealkiri | `12-14 pt`, tume |
| KPI väärtus | `24-32 pt`, tume |
| KPI silt | `10-12 pt`, hall |
| Annotatsioon | `10-12 pt`, rõhutuse värviga |
| Andmeloo tekst | `11-13 pt`, tume või hall |

#### Kiire kontroll enne esitamist

- Kas kõik automaatsed pealkirjad on muudetud arusaadavaks?
- Kas topeltpealkirjad on eemaldatud?
- Kas KPI kaartidel on inimesele loetavad nimed?
- Kas annotatsioonid ei kata graafiku olulisi punkte?
- Kas värvid on ühtsed?
- Kas tekst on piisavalt suur, et ekraanipildilt lugeda?
- Kas lehel on näha üks selge põhisõnum?

## 2. Mida vajad enne alustamist

Sul peab olema:

- Microsoft Power BI Desktop;
- eelmise nädala Power BI fail või ligipääs UrbanStyle Supabase andmetele;
- UrbanStyle tabelid `sales`, `products`, `customers` ja võimalusel `inventory`;
- meeskonnas kokkulepitud roll A, B, C või D.

Kui sul on eelmise nädala fail olemas, kasuta seda:

```text
week-05/team/urbanstyle_power_bi_week_5.pbix
```

Soovitus: ära kirjuta eelmise nädala faili üle. Salvesta nädal 6 töö uue failina.

## 3. Ava eelmise nädala Power BI fail ja salvesta koopia

1. Ava `Microsoft Power BI Desktop`.
2. Vali vasakult `Open`.
3. Vajuta `Browse this device`.
4. Ava eelmise nädala fail:
5. Kui fail on avanenud, vajuta üleval vasakul `File`.
6. Vali `Save as`.
7. Salvesta uus fail nädal 6 kausta:
8. Kontrolli, et Power BI ülemisel ribal oleks nüüd avatud nädal 6 fail.

## 4. Värskenda andmed

1. Vali üleval ribal `Home`.
2. Vajuta `Refresh`.
3. Oota, kuni Power BI andmed uuendab.
4. Kui avaneb andmeallika ühenduse aken, sisesta vajadusel Supabase ühenduse andmed.
5. Kui `Refresh` lõpeb veata, jätka järgmise sammuga.

Kui `Refresh` annab vea, aga eelmise nädala visualid näitavad andmeid, võid juhendi tegemist jätkata olemasoleva andmeseisuga.

## 5. Kontrolli põhimõõdikud üle

Enne uue vaate tegemist kontrolli, et vajalikud mõõdikud on olemas.

1. Mine `Report view` vaatesse.
2. Paremal `Data` paneelis ava tabel `sales`.
3. Kontrolli, kas olemas on vähemalt need mõõdikud:

| Mõõdik | Milleks kasutatakse |
|---|---|
| `Kogukäive` | KPI kaart ja müügitrend |
| `Tellimusi` | tellimuste arv |
| `Kliente` | klientide arv |
| `Keskmine tellimus` | keskmine ostukorv |
| `Müüdud ühikuid` | müügimahu võrdlus |

Kui mõõdikuid ei ole, loo need uuesti.

1. Tee paremal `Data` paneelis tabelil `sales` paremklõps.
2. Vali `New measure`.
3. Kopeeri valemiribale mõõdik.
4. Vajuta `Enter`.
5. Korda sama iga mõõdikuga.

```DAX
Kogukäive =
SUM ( sales[total_price] )
```

```DAX
Tellimusi =
DISTINCTCOUNT ( sales[invoice_id] )
```

```DAX
Kliente =
DISTINCTCOUNT ( sales[customer_id] )
```

```DAX
Keskmine tellimus =
DIVIDE ( [Kogukäive], [Tellimusi] )
```

```DAX
Müüdud ühikuid =
SUM ( sales[quantity] )
```

## 6. Kontrolli kuupäevaväli üle

Müügitrendi jaoks peab kuupäev töötama.

1. Paremal `Data` paneelis leia tabel `sales`.
2. Kontrolli, kas olemas on veerg `sale_date`.
3. Kui sul on eraldi kuupäevatabel `Date`, kasuta trendi X-teljel `Date[YearMonth]`.
4. Kui kuupäevatabelit ei ole, kasuta X-teljel `sales[sale_date]`.

Kui soovid kuupäevatabeli uuesti luua:

1. Vali ülevalt `Modeling`.
2. Vajuta `New table`.
3. Kopeeri valemiribale:

```DAX
Date =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2023, 1, 1 ), DATE ( 2025, 2, 28 ) ),
    "Year", YEAR ( [Date] ),
    "Month", FORMAT ( [Date], "MMM" ),
    "YearMonth", FORMAT ( [Date], "YYYY-MM" )
)
```

4. Vajuta `Enter`.
5. Mine vasakul `Model view`.
6. Lohista `Date[Date]` veerult seos `sales[sale_date]` veerule.

## 7. Loo oma rolli raportileht

1. All lehesakkide juures vajuta `+`.
2. Tee uuel lehesakil paremklõps.
3. Vali `Rename`.
4. Nimeta leht vastavalt oma rollile:

| Roll | Lehe nimi |
|---|---|
| A | `Tallinn` |
| B | `Tartu` |
| C | `Parnu` |
| D | `E-pood` |

5. Vajuta tühjale raportilehele.
6. Paremal `Format page` paneelis ava `Canvas settings`.
7. Kui vaja, vali formaadiks `16:9`.
8. Ava `Canvas background`.
9. Pane taustaks peaaegu valge või väga helehall.

Soovituslik stiil:

| Element | Seadistus |
|---|---|
| Page background | `#F8FAFA` või `#F6F7F8` |
| Visual background | `#F1F3F4` või `#EEF1F2` |
| Ülemine pealkirjariba | `#E3F5F3` või `#DDF3F1` |
| Soovituste ploki taust | `#E3F5F3` või `#DDF3F1` |
| Põhiaktsent, jooned ja nooled | `#18AFA5` või `#21B8AD` |
| Tume tekst ja KPI väärtused | `#1E2430` või `#2B2F3A` |
| Sekundaarne tekst ja sildid | `#7A858E` või `#8B949C` |
| Negatiivne rõhutus | crimson red `#DC143C` või tumedam crimson `#B11226` |
| Negatiivse ploki taust | hele crimson toon `#FDECEF` või `#F9DDE3` |
| Font | Segoe UI |

## 8. Lisa asukoha või kanali filter

### Roll A: Tallinn

1. Klõpsa tühjal raportilehel, mitte visualil.
2. Paremal `Filters` paneelis leia jaotis `Filters on this page`.
3. Lohista `sales[store_location]` jaotisse `Filters on this page`.
4. Ava filter.
5. Vali ainult `Tallinn`.
6. Kontrolli, et teised asukohad ei oleks valitud.

### Roll B: Tartu

1. Klõpsa tühjal raportilehel.
2. Lohista `sales[store_location]` jaotisse `Filters on this page`.
3. Ava filter.
4. Vali ainult `Tartu`.

### Roll C: Pärnu

1. Klõpsa tühjal raportilehel.
2. Lohista `sales[store_location]` jaotisse `Filters on this page`.
3. Ava filter.
4. Vali ainult `Pärnu`.

Kui Power BI näitab Pärnu nime täpitähtedeta, vali see variant, mis andmetes olemas on.

### Roll D: E-pood

E-poe puhul kasuta kanalifiltrit, sest online-müügil võib `store_location` olla tühi.

1. Klõpsa tühjal raportilehel.
2. Lohista `sales[channel]` jaotisse `Filters on this page`.
3. Ava filter.
4. Vali ainult `online`.

Kui andmetes on väärtus `Online`, `E-pood` või `web`, vali see variant, mis vastab online-müügile.

## 9. Lisa dashboard'i pealkiri

1. Vali ülevalt `Insert`.
2. Vajuta `Text box`.
3. Kirjuta pealkiri:

| Roll | Pealkiri |
|---|---|
| A | `Tallinna kaupluse andmelugu` |
| B | `Tartu kaupluse andmelugu` |
| C | `Pärnu kaupluse andmelugu` |
| D | `E-poe kasvulugu` |

4. Märgi tekst ära.
5. Vali fondiks `Segoe UI`.
6. Pane suuruseks umbes `22-26`.
7. Pane värviks `#1E2430`.
8. Lisa pealkirja taha hele mint/türkiis riba värviga `#E3F5F3`.
9. Paiguta pealkiri lehe ülemisse vasakusse nurka.

## 10. Lisa juhtide kokkuvõte

Juhtide kokkuvõte peab ütlema, mis toimub ja miks see oluline on.

1. Vali ülevalt `Insert`.
2. Vajuta `Text box`.
3. Paiguta tekstikast pealkirja alla või KPI kaartide kõrvale.
4. Kirjuta 3-5 lühikest järeldust.
5. Kui kokkuvõttes on eraldi soovitus, kasuta selle ploki taustaks `#E3F5F3` või `#DDF3F1`.
6. Pane põhiteksti värviks `#1E2430` ja väiksemate selgituste värviks `#7A858E`.

Kasuta seda vormi:

```text
Peamine järeldus:
- [Asukoht] kogukäive on [number või suund].
- Kõige tugevam kategooria on [kategooria].
- Suurim võimalus või risk on [võimalus/risk].
- Soovitus: [mida peaks Anna või juhatus tegema].
```

Näited rollide kaupa:

```text
Tallinn on UrbanStyle'i tugevaim müügikoht.
Kõige olulisem kasvuvõimalus on korrata Tallinna toimivaid kampaaniaid teistes asukohtades.
```

```text
Tartu müük vajab tähelepanu, sest trend on nõrgem kui teistes asukohtades.
Soovitus on kontrollida tootevalikut ja kampaaniate mõju Tartu klientidele.
```

```text
Pärnu müük on hooajaline ja sõltub tugevalt suvekuudest.
Soovitus on planeerida suvevaru varem ning otsida talveperioodi müügivõimalusi.
```

```text
E-pood on UrbanStyle'i skaleeritav kasvukanal.
Soovitus on suurendada digikanali investeeringuid, kui kasv ja keskmine tellimus seda toetavad.
```

## 11. Lisa KPI kaardid

Igal dashboard'il peaks üleval olema 3-4 KPI kaarti.

1. Vali paremal `Visualizations` paneelis `Card`.
2. Lohista `Kogukäive` väljale `Data` või `Fields`.
3. Paiguta kaart dashboard'i ülemisse ossa.
4. Tee sama järgmiste mõõdikutega:
   - `Tellimusi`
   - `Kliente`
   - `Keskmine tellimus`

Kaardi vormindamine:

1. Klõpsa kaardil.
2. Ava paremal `Format visual`.
3. Ava `Callout value`.
4. Pane värviks `#1E2430`.
5. Pane fondiks `Segoe UI`.
6. Ava `Category label`.
7. Pane värviks `#7A858E`.
8. Ava `General` > `Effects`.
9. Pane `Background` sisse ja värviks `#F1F3F4` või `#EEF1F2`.
10. Kui kasutad piire, pane `Border` väga helehalliks.
11. Kui lisad muutuse protsendi, näiteks `↑15%`, pane see värviga `#18AFA5`.

### 11.1. Lisa noolega callout

Kui tahad, et muutuse protsendi ette tuleks automaatselt üles- või allapoole nool, tee selleks eraldi measure.

Kui sul on juba olemas `Käive 2024` ja `Käive 2023`, tee uus measure:

```DAX
Käibe kasv noolega =
VAR Muutus =
    DIVIDE(
        [Käive 2024] - [Käive 2023],
        [Käive 2023]
    )
RETURN
SWITCH(
    TRUE(),
    Muutus > 0, "↑ " & FORMAT(Muutus, "0%"),
    Muutus < 0, "↓ " & FORMAT(ABS(Muutus), "0%"),
    "→ 0%"
)
```

Kasuta seda measure'it `Card` visualis samamoodi nagu tavalist KPI-d:

1. Vali `Card`.
2. Lohista `Käibe kasv noolega` väljale `Data` või `Fields`.
3. Pane kaardi pealkirjaks näiteks `Käibe muutus`.

Füüsilise poe puhul kasuta sõnastuses pigem `Müüke` või `Oste`. `Tellimusi` sobib rohkem e-poe kohta.

### 11.2. Muuda noole värvi automaatselt

Noole ja protsendi värvi jaoks tee teine measure:

```DAX
Käibe kasvu värv =
VAR Muutus =
    DIVIDE(
        [Käive 2024] - [Käive 2023],
        [Käive 2023]
    )
RETURN
SWITCH(
    TRUE(),
    Muutus > 0, "#18AFA5",
    Muutus < 0, "#D64545",
    "#777777"
)
```

Rakenda see `Card` visualile nii:

1. Klõpsa kaardil, kus on `Käibe kasv noolega`.
2. Ava paremal `Format visual`.
3. Ava `Callout value`.
4. Leia `Color` ja vajuta selle juures `fx`.
5. Pane `Format style` valikuks `Field value`.
6. Pane `Based on field` valikuks `Käibe kasvu värv`.
7. Vajuta `OK`.

Nüüd kuvab Power BI positiivse muutuse näiteks `↑ 15%` värviga `#18AFA5`, negatiivse muutuse punasega ja nullmuutuse halliga.

KPI kaartide soovituslikud pealkirjad:

| Mõõdik | Pealkiri |
|---|---|
| `Kogukäive` | `Kogukäive` |
| `Tellimusi` | `Tellimuste arv` |
| `Kliente` | `Klientide arv` |
| `Keskmine tellimus` | `Keskmine tellimus` |

## 12. Lisa müügitrendi joondiagramm

1. Vali `Visualizations` paneelis `Line chart`.
2. Paiguta diagramm dashboard'i keskmisse või vasakusse ossa.
3. Pane X-teljeks `Date[YearMonth]` või `sales[sale_date]`.
4. Pane Y-teljeks `Kogukäive`.
5. Klõpsa diagrammil.
6. Ava `Format visual`.
7. Ava `General` > `Title`.
8. Lülita pealkiri sisse.
9. Kirjuta pealkirjaks:

```text
Müügikäibe trend kuude lõikes
```

10. Ava `Visual` > `Lines`.
11. Pane joone värviks `#18AFA5` või `#21B8AD`.
12. Ava `X-axis` ja `Y-axis`.
13. Pane telgede ja siltide värviks `#7A858E` või `#8B949C`.
14. Kontrolli, et tekst oleks loetav.

Rollipõhine fookus:

| Roll | Mida trendist otsida |
|---|---|
| Tallinn | kas müük on stabiilselt tugev või kasvav |
| Tartu | kas müük langeb ja mis kuust alates |
| Pärnu | kas suvekuud on selgelt kõrgemad |
| E-pood | kas online-kasv on kiirem kui kauplustes |

## 13. Lisa TOP 5 toodete või kategooriate tulpdiagramm

1. Vali `Visualizations` paneelis `Clustered bar chart`.
2. Paiguta diagramm trendi kõrvale või alla.
3. Pane Y-teljeks `products[product_name]` või `products[category]`.
4. Pane X-teljeks `Kogukäive`.
5. Klõpsa visuali paremas ülemises nurgas kolme punkti peal.
6. Vali `Sort axis`.
7. Vali `Kogukäive`.
8. Vali `Sort descending`.
9. Ava paremal `Filters on this visual`.
10. Lohista sama väli, mida kasutad Y-teljel, filtrisse.
11. Vali `Filter type` väärtuseks `Top N`.
12. Sisesta `5`.
13. Lohista `Kogukäive` väljale `By value`.
14. Vajuta `Apply filter`.

Pane pealkirjaks:

```text
TOP 5 tooted kogukäibe järgi
```

Kui tootenimed on liiga pikad, kasuta kategooriat ja pane pealkirjaks:

```text
Käive kategooriate lõikes
```

## 14. Lisa kliendisegmentide visual

Kui tabelis `customers` on olemas `loyalty_tier`, tee kliendisegmentide vaade.

1. Vali `Visualizations` paneelis `Clustered column chart`.
2. Pane X-teljeks `customers[loyalty_tier]`.
3. Pane Y-teljeks `Kogukäive` või `Kliente`.
4. Pane pealkirjaks:

```text
Kliendisegmendid müügikäibe järgi
```

Kui `loyalty_tier` puudub, kasuta `customers[city]` või jäta see visual ära ja lisa selle asemel makseviisi või kanali visual.

## 15. Lisa rollipõhine lisavisual

Vali üks lisavisual vastavalt oma rollile.

### Roll A: Tallinn

Tallinna puhul lisa kanalite või kategooriate võrdlus.

1. Lisa `Clustered column chart`.
2. Pane X-teljeks `sales[channel]`.
3. Pane Y-teljeks `Kogukäive`.
4. Pane pealkirjaks:

```text
Tallinna müük kanalite lõikes
```

### Roll B: Tartu

Tartu puhul lisa võrdlus või probleemikoht.

1. Lisa `Clustered column chart`.
2. Pane X-teljeks `products[category]`.
3. Pane Y-teljeks `Kogukäive`.
4. Pane pealkirjaks:

```text
Tartu tugevamad ja nõrgemad kategooriad
```

Kui soovid võrrelda Tartuga Tallinna keskmist, tee see juhtide kokkuvõttes tekstina või lisa viitejoon trendile.

### Roll C: Pärnu

Pärnu puhul lisa hooajaline võrdlus.

1. Lisa `Clustered column chart`.
2. Pane X-teljeks `Date[Month]`.
3. Pane Y-teljeks `Kogukäive`.
4. Pane pealkirjaks:

```text
Pärnu hooajalisus kuude lõikes
```

### Roll D: E-pood

E-poe puhul lisa kanalite osakaal.

1. Lisa `Donut chart` või `Clustered column chart`.
2. Pane legendiks või X-teljeks `sales[channel]`.
3. Pane väärtuseks `Kogukäive`.
4. Pane pealkirjaks:

```text
E-poe osakaal kogukäibest
```

Kui lehel on juba `channel = online` filter, tee see visual pigem eraldi koondlehele ilma page-level filtrita. Oma e-poe lehel kasuta selle asemel toodete või kuude kasvu visuali.

## 16. Lisa viitejoon

Viitejoon aitab vaatajal aru saada, kas tulemus on üle või alla ootuse.

Lihtsaim variant on lisada viitejoon müügitrendi joondiagrammile.

1. Klõpsa `Müügikäibe trend kuude lõikes` visualil.
2. Paremal `Visualizations` paneelis vali `Analytics`.
3. Leia `Y-axis constant line`.
4. Vajuta `Add line`.
5. Pane joone väärtuseks eesmärk või keskmine.

Kui sa ei tea eesmärki, kasuta ligikaudset keskmist:

1. Vaata trendi pealt, mis on tavaline kuukäibe tase.
2. Sisesta see number viitejoone väärtuseks.
3. Pane joone nimeks `Keskmine kuukäive` või `Eesmärk`.

Vorminda viitejoon:

1. Pane joone värviks `#18AFA5` või `#21B8AD`.
2. Pane joone stiiliks katkeline joon, kui see valik on olemas.
3. Lülita `Data label` sisse.
4. Kirjuta labeliks näiteks:

```text
Keskmine kuukäive
```

Rollipõhised viitejoone ideed:

| Roll | Viitejoone idee |
|---|---|
| Tallinn | keskmine kuukäive või kvartalieesmärk |
| Tartu | Tallinna keskmine võrdluspunktina või Tartu eesmärk |
| Pärnu | aasta keskmine kuukäive või suveeesmärk |
| E-pood | online-kasvueesmärk või füüsiliste poodide keskmine |

## 17. Lisa annotatsioonid

Annotatsioon peab selgitama, miks üks number või muutus on oluline.

Power BI-s tee annotatsioon tekstikastiga.

1. Vali ülevalt `Insert`.
2. Vajuta `Text box`.
3. Kirjuta lühike märkus.
4. Paiguta tekstikast selle visuali kõrvale või peale, mida märkus selgitab.
5. Tee tekst väiksemaks kui pealkiri, näiteks `10-12 pt`.
6. Kasuta rõhutuseks värvi `#18AFA5` või `#21B8AD`.
7. Kui lisad noole, tee nool sama türkiissinise aktsendiga.
8. Negatiivse muutuse puhul kasuta rõhutuseks crimson red tooni `#DC143C` või tumedamat crimson tooni `#B11226`.
9. Kui negatiivne tähelepanek on eraldi tekstiplokis, kasuta taustaks heledat crimson tooni `#FDECEF` või `#F9DDE3`.

Lisa vähemalt 2 annotatsiooni.

Head annotatsiooni näited:

```text
Jõulukampaania tipp: müük kasvas võrreldes eelmise kuuga.
```

```text
Langustrend algab kevadel, seega vajab Tartu kampaaniaplaan ülevaatamist.
```

```text
Suvekuud annavad suure osa Pärnu aastakäibest.
```

```text
Black Friday tõi e-poele nähtava müügihüppe.
```

Negatiivse rõhutuse näited:

```text
Müük langes kolm kuud järjest, seega vajab kampaaniaplaan ülevaatamist.
```

```text
Keskmine tellimus on alla eesmärgi, mis võib vähendada kogu kuu kasumlikkust.
```

```text
Laoseis ei toeta müügitrendi: populaarsete toodete varu võib lõppeda enne tipphooaega.
```

```text
E-poe kasv aeglustus pärast kampaaniat, seega ei pruugi ühekordne allahindlus püsivat nõudlust näidata.
```

Väldi selliseid annotatsioone:

```text
Käive: 85000.
```

```text
Siin on suur tulp.
```

Annotatsioon peab vastama küsimusele: "Ja mis siis?"

## 18. Kirjuta andmelugu

Andmelugu kirjuta 3-4 lausega. Lisa see dashboard'ile tekstikastina või eraldi Markdown-failina.

Kasuta seda struktuuri:

```text
[Asukoht] on UrbanStyle'i jaoks [roll või tähendus].
Dashboard näitab, et [peamine fakt andmetest].
See tähendab, et [äriline tõlgendus].
Soovitame [tegevus], sest [põhjus].
```

Roll A näide:

```text
Tallinn on UrbanStyle'i suurim ja kõige olulisem füüsiline kauplus.
Dashboard näitab, et Tallinna müük on tugev ning peamised kategooriad annavad suure osa kogukäibest.
See tähendab, et Tallinn võib olla mudel, mille toimivaid kampaaniaid ja tootevalikut saab testida ka teistes asukohtades.
Soovitame hoida Tallinna tugevamate kategooriate laoseisu ning kasutada sealt saadud õppetunde Tartu ja Pärnu parandamiseks.
```

Roll B näide:

```text
Tartu on UrbanStyle'i teine füüsiline kauplus, kuid selle tulemused vajavad tähelepanu.
Dashboard näitab, millistel kuudel või kategooriates on müük nõrgem.
See tähendab, et probleem ei pruugi olla ainult üldises nõudluses, vaid ka tootevalikus, kampaaniates või kohalikus konkurentsis.
Soovitame analüüsida Tartu klientide ostukäitumist ja testida sihitud kampaaniat.
```

Roll C näide:

```text
Pärnu on UrbanStyle'i hooajaline kauplus, mille tulemused sõltuvad tugevalt suveperioodist.
Dashboard näitab, kas juuni, juuli ja august annavad suure osa aastakäibest.
See tähendab, et Pärnu edukus sõltub õigest varude ja kampaaniate ajastamisest.
Soovitame planeerida suvekollektsiooni ja reklaami varem ning otsida talveperioodiks eraldi müügipakkumisi.
```

Roll D näide:

```text
E-pood on UrbanStyle'i kõige skaleeritavam müügikanal.
Dashboard näitab, kas online-müük kasvab ja millised tooted digikanalis kõige paremini toimivad.
See tähendab, et e-pood võib anda UrbanStyle'ile kasvu ilma uute füüsiliste kaupluste avamiseta.
Soovitame suurendada digikanali kampaaniaid ja jälgida, kas logistika suudab kasvu toetada.
```

## 19. Kontrolli dashboard'i kvaliteeti

Enne meeskonnale esitamist kontrolli:

- Dashboard näitab ainult sinu rolli andmeid.
- Lehel on 3-5 visuali.
- Üleval on 3-4 KPI kaarti.
- Juhtide kokkuvõte sisaldab 3-5 järeldust.
- Vähemalt 2 annotatsiooni selgitavad, miks tulemus on oluline.
- Vähemalt 1 viitejoon on lisatud.
- Andmelugu on 3-4 lauset.
- Kõik pealkirjad on selged.
- Teljed ja sildid on loetavad.
- Värvid on ühtsed.
- Leht ei ole liiga täis.

## 20. Esitle oma tulemus meeskonnale

Kui igaüks on oma dashboard'i valmis saanud, esitle seda meeskonnale 2-3 minutiga.

Kasuta seda formaati:

```text
Mina vaatasin [asukoha või kanali nimi] andmeid.
Leidsin, et [peamine tulemus].
See tähendab UrbanStyle'ile, et [äriline tõlgendus].
Minu soovitus on [tegevus].
```

Näide:

```text
Mina vaatasin Pärnu kaupluse andmeid.
Leidsin, et müük on tugevalt hooajaline ja suvekuud mõjutavad aastakäivet kõige rohkem.
See tähendab UrbanStyle'ile, et Pärnu tulemus sõltub väga palju õigel ajal planeeritud varudest ja kampaaniatest.
Minu soovitus on teha Pärnule eraldi suvehooaja müügiplaan.
```

## 21. Koosta meeskonna koondvaade

Koondvaade tehke Google Slides'is või Power BI eraldi lehel.

### Variant A: Google Slides

1. Avage meeskonna Google Slides fail.
2. Looge uus slide.
3. Pange pealkirjaks:

```text
UrbanStyle asukohtade koondlugu
```

4. Lisage nelja liikme ekraanipildid või kokkuvõtted.
5. Kirjutage iga asukoha kohta 1 rida:

```text
Tallinn: [2-3 sõna kokkuvõte] + [peamine number]
Tartu: [2-3 sõna kokkuvõte] + [peamine number]
Pärnu: [2-3 sõna kokkuvõte] + [peamine number]
E-pood: [2-3 sõna kokkuvõte] + [peamine number]
```

6. Lisage üks koondlause:

```text
UrbanStyle'i asukohad näitavad, et [peamine meeskonna järeldus].
```

7. Lisage soovitus Annale:

```text
Soovitame Annal [tegevus], sest [põhjus].
```

### Variant B: Power BI koondleht

1. Power BI all lehesakkide juures vajuta `+`.
2. Nimeta leht `Koondvaade`.
3. Ära pane sellele lehele asukoha page-level filtrit.
4. Lisa `Clustered column chart`.
5. Pane X-teljeks `sales[store_location]`.
6. Pane Y-teljeks `Kogukäive`.
7. Lisa teine visual `Line chart`.
8. Pane X-teljeks `Date[YearMonth]`.
9. Pane Y-teljeks `Kogukäive`.
10. Pane legendiks `sales[store_location]`.
11. Lisa KPI kaardid `Kogukäive`, `Tellimusi`, `Kliente`.
12. Lisa tekstikast koondjäreldusega.

Kui online-müügil ei ole `store_location` väärtust, kasuta koondvaates `sales[channel]` või tee online kohta eraldi tekstirida.

## 22. Vasta sünteesiküsimustele

Meeskond peab lõpus vastama kolmele küsimusele.

Kopeerige need Google Slides'i, ühisdokumenti või portfoolio märkmetesse.

```text
1. Mis oli suurim üllatus, kui võrdlesime nelja asukohta?

Vastus:

2. Milline on meie soovitus Annale UrbanStyle'i asukohtade strateegia kohta?

Vastus:

3. Milliseid andmeid meil puudus, et anda Annale veel paremat nõu?

Vastus:
```

Puuduvate andmete näited:

- konkurentide andmed;
- kliendirahulolu;
- kampaaniakulud;
- logistikakulud;
- tööjõukulud asukohati;
- kaupluste külastajate arv;
- e-poe konversioonimäär.

## 23. Tee ekraanipilt

1. Ava valmis dashboard'i leht Power BI-s.
2. Vajuta klaviatuuril `Windows` + `Shift` + `S`.
3. Vali ainult dashboard'i ala.
4. Salvesta pilt nädal 6 kausta.

Soovituslikud failinimed:

```text
week6_roll_a_tallinn_dashboard.png
week6_roll_b_tartu_dashboard.png
week6_roll_c_parnu_dashboard.png
week6_roll_d_epood_dashboard.png
week6_team_koondvaade.png
```

## 24. Lisa portfooliosse

Iga osaleja lisab oma portfooliosse:

- dashboard'i ekraanipildi;
- 3-4-lauselise andmeloo;
- executive summary ehk 3-5 järeldust;
- AI kasutamise kirjelduse.

Soovituslik Markdown tekst:

```markdown
# Nädal 6: Asukohapõhine andmelugu

## Minu roll

Minu roll oli [Tallinn / Tartu / Pärnu / E-pood].

## Dashboard

![Dashboard](week6_roll_x_dashboard.png)

## Juhtide kokkuvõte

- [Järeldus 1]
- [Järeldus 2]
- [Järeldus 3]

## Andmelugu

[Kirjuta siia 3-4 lauset.]

## Meeskonna koondvaade

Meie meeskond analüüsis UrbanStyle'i nelja asukohta. Minu panus oli [asukoht või kanal] dashboard ja narratiiv.

## AI kasutamine

Kasutasin AI-d annotatsioonide sõnastamiseks ja andmeloo lihvimiseks. Kontrollisin, et AI pakutud järeldused vastaksid tegelikele Power BI andmetele.
```

## 25. AI kasutamine

AI-d võib kasutada:

- annotatsioonide sõnastamiseks;
- andmeloo esimese mustandi kirjutamiseks;
- Power BI DAX mõõdikute kontrollimiseks;
- dashboard'i ülesehituse ideede saamiseks;
- esitluse teksti lühendamiseks.

AI kasutamisel kontrolli alati:

- kas number vastab Power BI visualile;
- kas filter on õige asukoha või kanali peal;
- kas AI ei mõelnud juurde põhjuseid, mida andmetes ei ole;
- kas soovitus on seotud tegeliku järeldusega.

Sobiv AI prompt:

```text
Mul on UrbanStyle'i [Tallinn/Tartu/Pärnu/e-pood] dashboard.
Peamised leiud on: [kirjuta 2-3 fakti].
Palun aita kirjutada 3-4-lauseline andmelugu, mis sisaldab ülesseadet, andmeid, ärilist tõlgendust ja soovitust.
Ära mõtle uusi numbreid juurde.
```

## 26. Kui midagi ei tööta

| Probleem | Lahendus |
|---|---|
| Leht näitab kõiki asukohti | Kontrolli `Filters on this page` ja vali ainult oma asukoht |
| E-pood ei ilmu store_location filtriga | Kasuta `sales[channel] = online` filtrit |
| Trend on tühi | Kontrolli kuupäevavälja ja seost kuupäevatabeliga |
| TOP 5 ei tööta | Vajuta visuali filtris `Apply filter` |
| Kaardil on tühi väärtus | Kontrolli, kas mõõdik kasutab õiget tabelit ja filter ei eemalda kõiki ridu |
| Annotatsioon ei püsi õiges kohas | Paiguta tekstikast visuali kõrvale, mitte liiga täpselt punkti peale |
| Viitejoone väärtus tundub vale | Kasuta eesmärki, keskmist või kirjuta tekstis, et see on hinnanguline võrdluspunkt |
| Dashboard on liiga kirju | Eemalda liigsed sildid, kasuta vähem värve ja jäta alles ainult põhisõnumit toetavad visualid |

## 27. Lõplik checklist

Enne esitamist kontrolli:

- [ ] Power BI fail on salvestatud nädal 6 kausta.
- [ ] Minu raportileht on nimetatud rolli järgi.
- [ ] Page-level filter näitab õiget asukohta või kanalit.
- [ ] Dashboard'il on 3-5 visuali.
- [ ] KPI kaardid on olemas.
- [ ] Müügitrendi joondiagramm on olemas.
- [ ] TOP 5 toodete või kategooriate visual on olemas.
- [ ] Juhtide kokkuvõte on lisatud.
- [ ] Vähemalt 2 annotatsiooni on lisatud.
- [ ] Vähemalt 1 viitejoon on lisatud.
- [ ] Andmelugu on 3-4 lauset.
- [ ] Ekraanipilt on salvestatud.
- [ ] Meeskonna koondvaade on koostatud.
- [ ] Sünteesiküsimustele on vastatud.
- [ ] AI kasutamine on portfoolios kirjeldatud.
