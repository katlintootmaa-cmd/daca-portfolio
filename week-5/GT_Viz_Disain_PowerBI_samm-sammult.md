# GT_Viz_Disain grupitöö: Power BI Desktop samm-sammult juhend

Versioon: Microsoft Power BI Desktop 2.153.910.0 64-bit, April 2026  
Töö: DACA nädal 5, visualiseerimise disain, grupitöö  
Andmed: UrbanStyle CSV failid sinu repos kaustas `SQL`

## 1. Eesmärk

Grupitöö eesmärk on teha samade UrbanStyle andmete põhjal mitu erinevat dashboard'i, sest eri stakeholder'id küsivad eri küsimusi.

Stakeholder'id:

| Roll | Vaade | Põhiküsimus |
|---|---|---|
| A | CEO / Kristi | Kas UrbanStyle kasvab? |
| B | Marketing / Anna | Kas müügikanalid töötavad? |
| C | Operations / Liis | Kas laoseis ja poed toimivad? |
| D | Investor | Kas UrbanStyle on investeerimisväärne? |

Miinimumtulemus iga inimese kohta:

- 2 diagrammi oma stakeholder'ile.
- Selged pealkirjad, sildid ja värvid.
- 1-2 lauset äritõlgendust iga diagrammi kohta.
- Ekraanipilt Google Slides'i / portfoolio jaoks.

## 2. Kasutatavad failid

Kasuta neid CSV faile:

```text
C:\Users\Kätlin\Documents\Õppeprojekt\daca-portfolio\SQL\sales_rows.csv
C:\Users\Kätlin\Documents\Õppeprojekt\daca-portfolio\SQL\customers.csv
C:\Users\Kätlin\Documents\Õppeprojekt\daca-portfolio\SQL\products.csv
C:\Users\Kätlin\Documents\Õppeprojekt\daca-portfolio\SQL\inventory.csv
```

Kui Power BI küsib encodingut, vali `65001: Unicode (UTF-8)`.

## 3. Ava Power BI ja alusta uut faili

1. Ava `Microsoft Power BI Desktop`.
2. Kui avaneb start-aken, vajuta `Blank report`.
3. Üleval ribal kontrolli, et oled vaates `Home`.
4. Salvesta kohe algfail:
   - Vajuta vasakul üleval `File`.
   - Vali `Save as`.
   - Salvesta näiteks:

```text
C:\Users\Kätlin\Documents\Õppeprojekt\daca-portfolio\week-5\gt_viz_disain_urbanstyle.pbix
```

## 4. Impordi CSV andmed

Tee järgmised sammud iga CSV faili kohta.

1. Üleval ribal vali `Home`.
2. Vajuta `Get data`.
3. Vali `Text/CSV`.
4. Ava esimene fail `sales_rows.csv`.
5. Eelvaate aknas kontrolli:
   - `File Origin`: `65001: Unicode (UTF-8)`, kui see valik on olemas.
   - `Delimiter`: `Comma`.
6. Vajuta `Transform Data`, mitte `Load`.

Power Query Editor avaneb.

Nüüd lisa teised tabelid:

1. Power Query Editoris vali ülevalt `Home`.
2. Vajuta `New Source`.
3. Vali `Text/CSV`.
4. Ava `customers.csv`.
5. Vajuta `OK`.
6. Korda sama failidega `products.csv` ja `inventory.csv`.

Kui kõik 4 tabelit on vasakul Queries nimekirjas olemas, jätka puhastamisega.

## 5. Nimeta tabelid selgelt

Power Query Editoris vasakul `Queries` paneelis:

1. Tee paremklõps `sales_rows`.
2. Vali `Rename`.
3. Nimeta tabeliks `sales`.
4. Kontrolli, et teised nimed oleksid:
   - `customers`
   - `products`
   - `inventory`

Kui mõni nimi on vale, tee paremklõps tabeli nimel ja vali `Rename`.

## 6. Kontrolli andmetüübid Power Querys

Vali vasakult tabel `sales`.

Kontrolli veergude päistes andmetüübi ikooni. Vajadusel vajuta veeru päises olevale andmetüübi ikoonile ja vali õige tüüp.

`sales` tabel:

| Veerg | Tüüp Power BI-s |
|---|---|
| sale_id | Whole Number |
| invoice_id | Text |
| sale_date | Date/Time |
| customer_id | Whole Number |
| product_id | Whole Number |
| quantity | Whole Number |
| unit_price | Decimal Number |
| total_price | Decimal Number |
| channel | Text |
| store_location | Text |
| payment_method | Text |

`customers` tabel:

| Veerg | Tüüp |
|---|---|
| customer_id | Whole Number |
| first_name | Text |
| last_name | Text |
| city | Text |
| registration_date | Date |
| loyalty_tier | Text |
| birth_year | Whole Number |

`products` tabel:

| Veerg | Tüüp |
|---|---|
| product_id | Whole Number |
| product_name | Text |
| category | Text |
| subcategory | Text |
| supplier | Text |
| cost_price | Decimal Number |
| retail_price | Decimal Number |
| eco_certified | True/False |
| created_at | Date |

`inventory` tabel:

| Veerg | Tüüp |
|---|---|
| inventory_id | Whole Number |
| product_id | Whole Number |
| location | Text |
| quantity_available | Whole Number |
| reorder_point | Whole Number |
| last_updated | Date |

## 7. Tee vajalikud puhastused

### 7.1. Puhasta `sales` tabel

1. Vali vasakult `sales`.
2. Vali veerg `total_price`.
3. Üleval vali `Home` > `Remove Rows` > `Remove Errors`, kui veerus on vigu.
4. Vali veerg `sale_date`.
5. Üleval vali `Home` > `Remove Rows` > `Remove Errors`, kui kuupäevades on vigu.

Kui soovid negatiivsed tagastused välja jätta:

1. Vali veeru `total_price` päises filtrinool.
2. Vali `Number Filters`.
3. Vali `Greater Than...`.
4. Sisesta `0`.
5. Vajuta `OK`.

Kui soovid tagastused alles jätta, ära seda filtrit rakenda. Grupitöö jaoks on lihtsam jätta ainult positiivsed müügid.

### 7.2. Puhasta `store_location`

1. Vali `sales` tabelis veerg `store_location`.
2. Üleval vali `Transform`.
3. Vajuta `Format`.
4. Vali `Trim`.
5. Vajuta uuesti `Format`.
6. Vali `Clean`.

Online müükidel võib `store_location` olla tühi. Selle parandamiseks:

1. Vali veerg `store_location`.
2. Üleval vali `Transform`.
3. Vajuta `Replace Values`.
4. `Value To Find`: jäta tühjaks.
5. `Replace With`: kirjuta `Online`.
6. Vajuta `OK`.

Kui tühja väärtuse asendamine nii ei toimi, tee hiljem DAX mõõdikutes `COALESCE` asemel visuali filtrites online kanal eraldi.

### 7.3. Puhasta `customers.city`

1. Vali vasakult `customers`.
2. Vali veerg `city`.
3. Üleval vali `Transform`.
4. Vajuta `Format` > `Trim`.
5. Vajuta `Format` > `Clean`.

## 8. Laadi andmed raportisse

1. Power Query Editoris vali ülevalt vasakult `Home`.
2. Vajuta `Close & Apply`.
3. Oota, kuni Power BI laeb andmed mudelisse.

## 9. Loo tabelite seosed

1. Vasakul küljeribal vajuta `Model view` ikooni.
2. Kui Power BI pole seoseid automaatselt loonud, loo need käsitsi lohistades.

Seosed:

| Seos | Kardinaalsus | Suund |
|---|---|---|
| `customers[customer_id]` -> `sales[customer_id]` | One-to-many | Single |
| `products[product_id]` -> `sales[product_id]` | One-to-many | Single |
| `products[product_id]` -> `inventory[product_id]` | One-to-many | Single |

Kui pead seost käsitsi muutma:

1. Tee seose joonel topeltklõps.
2. `Cardinality`: vali `One to many (*:1)` või `One-to-many (1:*)`, sõltuvalt Power BI kuvast.
3. `Cross filter direction`: vali `Single`.
4. Vajuta `OK`.

## 10. Loo kuupäevatabel

1. Mine vasakult `Data view`.
2. Üleval vali `Table tools`.
3. Vajuta `New table`.
4. Sisesta valemiribale:

```DAX
Date =
ADDCOLUMNS (
    CALENDAR ( MIN ( sales[sale_date] ), MAX ( sales[sale_date] ) ),
    "Year", YEAR ( [Date] ),
    "Month Number", MONTH ( [Date] ),
    "Month", FORMAT ( [Date], "MMM yyyy" ),
    "YearMonth", FORMAT ( [Date], "yyyy-MM" )
)
```

5. Vajuta `Enter`.
6. Mine `Model view`.
7. Lohista `Date[Date]` veerg `sales[sale_date]` peale.
8. Kui Power BI küsib seose sätteid:
   - `Cardinality`: `One-to-many`.
   - `Cross filter direction`: `Single`.
   - Vajuta `OK`.

Kui `sales[sale_date]` on Date/Time ja seos ei teki, tee Power Querys eraldi kuupäevaveerg:

1. `Transform data`.
2. Vali `sales`.
3. Vali `sale_date`.
4. Üleval `Add Column` > `Date` > `Date Only`.
5. Nimeta uus veerg `sale_date_only`.
6. `Close & Apply`.
7. Seo `Date[Date]` veeruga `sales[sale_date_only]`.

## 11. Loo mõõdikud

1. Mine vasakult `Report view`.
2. Paremal `Data` paneelis tee paremklõps tabelil `sales`.
3. Vali `New measure`.
4. Lisa mõõdikud ükshaaval.

### 11.1. Üldmõõdikud

```DAX
Kogutulu = SUM ( sales[total_price] )
```

```DAX
Tellimusi = DISTINCTCOUNT ( sales[invoice_id] )
```

```DAX
Kliente = DISTINCTCOUNT ( sales[customer_id] )
```

```DAX
Keskmine tellimus = DIVIDE ( [Kogutulu], [Tellimusi] )
```

```DAX
Müüdud kogus = SUM ( sales[quantity] )
```

### 11.2. Kasvu mõõdikud

```DAX
Kogutulu eelmine aasta =
CALCULATE (
    [Kogutulu],
    SAMEPERIODLASTYEAR ( 'Date'[Date] )
)
```

```DAX
Kasv YoY % =
DIVIDE ( [Kogutulu] - [Kogutulu eelmine aasta], [Kogutulu eelmine aasta] )
```

Kui see mõõdik näitab tühja väärtust, siis sinu valitud perioodil puudub eelmine aasta. Investorivaates võid kasutada lihtsalt kogutulu ja kuist trendi.

### 11.3. Laoseisu mõõdikud

Tee need mõõdikud paremklõpsuga tabelile `inventory` > `New measure`.

```DAX
Laos kokku = SUM ( inventory[quantity_available] )
```

```DAX
Tellimuspunkt kokku = SUM ( inventory[reorder_point] )
```

```DAX
Alla tellimuspunkti =
COUNTROWS (
    FILTER (
        inventory,
        inventory[quantity_available] < inventory[reorder_point]
    )
)
```

```DAX
Laoriski % =
DIVIDE ( [Alla tellimuspunkti], COUNTROWS ( inventory ) )
```

### 11.4. Kasum ja marginaal

Tee need mõõdikud tabelile `sales`.

```DAX
Omahind kokku =
SUMX (
    sales,
    sales[quantity] * RELATED ( products[cost_price] )
)
```

```DAX
Brutokasum = [Kogutulu] - [Omahind kokku]
```

```DAX
Brutomarginaal % = DIVIDE ( [Brutokasum], [Kogutulu] )
```

## 12. Vorminda mõõdikud

1. Mine `Data view`.
2. Vali paremal mõõdik `Kogutulu`.
3. Üleval `Measure tools`.
4. `Format`: vali `Currency`.
5. `Currency symbol`: vali `€`, kui olemas.
6. `Decimal places`: `0` või `2`.

Tee sama:

| Mõõdik | Format |
|---|---|
| Kogutulu | Currency |
| Keskmine tellimus | Currency |
| Omahind kokku | Currency |
| Brutokasum | Currency |
| Kasv YoY % | Percentage |
| Brutomarginaal % | Percentage |
| Laoriski % | Percentage |

## 13. Ühine disainireegel kõigile lehtedele

UrbanStyle värvid:

| Kasutus | Värv |
|---|---|
| Peamine teal | `#009B8D` |
| Tume tekst / navy | `#1A1A2E` |
| Positiivne roheline | `#2F8F5B` |
| Hoiatus amber | `#D9902F` |
| Risk punane | `#C84C61` |
| Taust helehall | `#F5F7F8` |

Igal raportilehel:

1. Vali tühi raportileht.
2. Klõpsa tühjale lõuendile.
3. Paremal `Visualizations` paneelis vali `Format page`.
4. Ava `Canvas background`.
5. Vali värv `#F5F7F8`.
6. `Transparency`: `0%`.
7. Lisa pealkiri:
   - Üleval `Insert` > `Text box`.
   - Kirjuta lehe pealkiri.
   - Font: `Segoe UI` või `Arial`.
   - Värv: `#1A1A2E`.

Soovituslik paigutus:

- KPI kaardid üleval.
- Peamine diagramm keskel.
- Teine diagramm või filter all.
- Ära kasuta 3D efekte.
- Hoia diagrammid ühel ekraanil, ilma kerimiseta.

## 14. Roll A: CEO dashboard Kristile

Kristi küsimus: kas UrbanStyle kasvab?

### 14.1. Loo uus leht

1. All lehesakkidel vajuta `+`.
2. Tee lehesakil paremklõps.
3. Vali `Rename`.
4. Nimeta leht `A_CEO_Kristi`.

### 14.2. Lisa KPI kaardid

Lisa 4 KPI kaarti:

1. Paremal `Visualizations` paneelis vali `Card` visual.
2. Lohista `Kogutulu` väljale `Data`.
3. Paremal `Format visual` > `General` > `Title`.
4. Lülita `Title` sisse.
5. `Title text`: `Kogutulu`.
6. `Callout value`: vali suur font, näiteks 28-36.
7. Paiguta kaart lehe ülaossa.

Korda sama mõõdikutega:

- `Kliente`, pealkiri `Kliente`.
- `Tellimusi`, pealkiri `Tellimusi`.
- `Kasv YoY %`, pealkiri `Kasv YoY`.

Kui `Kasv YoY %` on tühi, kasuta selle asemel `Keskmine tellimus`.

### 14.3. Lisa müügitulu trend

1. Vali tühi koht lehel.
2. Paremal `Visualizations` paneelis vali `Line chart`.
3. Pane väljadele:
   - `X-axis`: `Date[YearMonth]`.
   - `Y-axis`: `Kogutulu`.
4. Visuali paremas ülanurgas vajuta `...`.
5. Vali `Sort axis`.
6. Vali `YearMonth`.
7. Vali `Sort ascending`.

Vormindus:

1. Vali joondiagramm.
2. Paremal `Format visual`.
3. Ava `Visual` > `Lines`.
4. Värv: `#009B8D`.
5. Ava `General` > `Title`.
6. `Title text`: `UrbanStyle müügitulu trend kuude lõikes`.
7. Ava `Visual` > `Y-axis`.
8. `Title`: `On`.
9. Y-axis title: `Müügitulu (€)`.

### 14.4. Lisa teine CEO diagramm: müük kategooriate lõikes

1. Vali tühi koht.
2. Vali `Clustered bar chart`.
3. Pane väljadele:
   - `Y-axis`: `products[category]`.
   - `X-axis`: `Kogutulu`.
4. Visuali `...` > `Sort axis` > `Kogutulu` > `Sort descending`.
5. `Format visual` > `General` > `Title`: `Müügitulu kategooriate lõikes`.
6. `Format visual` > `Visual` > `Bars` > `Colors`: `#009B8D`.

### 14.5. Kristi äritõlgendus

Lisa lehele tekstikast:

1. Üleval `Insert` > `Text box`.
2. Kirjuta näiteks:

```text
Müügitulu trend näitab, kas UrbanStyle kasvab kuude lõikes ja millal toimuvad suuremad hüpped või langused.
Kategooriate võrdlus näitab, millised tootegrupid veavad müügitulu ja kuhu tasub juhtkonnal fookus panna.
```

## 15. Roll B: Marketing dashboard Annale

Anna küsimus: kas müügikanalid töötavad?

### 15.1. Loo uus leht

1. All vajuta `+`.
2. Tee lehesakil paremklõps > `Rename`.
3. Nimi: `B_Marketing_Anna`.

### 15.2. Lisa müük kanalite lõikes

1. Vali `Clustered column chart`.
2. Pane väljadele:
   - `X-axis`: `sales[channel]`.
   - `Y-axis`: `Kogutulu`.
3. `...` > `Sort axis` > `Kogutulu` > `Sort descending`.
4. `Format visual` > `General` > `Title`: `Müügikanalite efektiivsus`.
5. `Format visual` > `Visual` > `Columns` > `Colors`:
   - peamine värv `#009B8D`.

### 15.3. Lisa klientide arv kanalite lõikes

1. Vali `Clustered bar chart`.
2. Pane väljadele:
   - `Y-axis`: `sales[channel]`.
   - `X-axis`: `Kliente`.
3. `Format visual` > `General` > `Title`: `Klientide arv müügikanalite lõikes`.

### 15.4. Lisa kuine kanalitrend

1. Vali `Line chart`.
2. Pane väljadele:
   - `X-axis`: `Date[YearMonth]`.
   - `Y-axis`: `Kogutulu`.
   - `Legend`: `sales[channel]`.
3. `Format visual` > `General` > `Title`: `Müügitulu trend kanalite lõikes`.
4. `Format visual` > `Visual` > `Lines`:
   - `pood`: `#009B8D`.
   - `online`: `#3B6EA8`, kui Power BI lubab seeriate kaupa muuta.

### 15.5. Lisa slicer kanalite või linna jaoks

1. Vali `Slicer` visual.
2. Lohista väljale `Field`: `sales[channel]`.
3. `Format visual` > `Slicer settings`.
4. `Style`: vali `Tile` või `Dropdown`.
5. Pealkiri: `Kanal`.

Soovi korral lisa teine slicer:

- `customers[city]`, pealkiri `Kliendi linn`.

### 15.6. Anna äritõlgendus

Lisa `Insert` > `Text box`:

```text
Kanalite võrdlus näitab, milline müügikanal toob kõige suurema käibe ja kliendibaasi.
Kui pood toob suurema käibe, kuid online kasvatab palju kliente, on soovitus parandada online ostukorvi väärtust ja konversiooni.
```

## 16. Roll C: Operations dashboard Liisile

Liisi küsimus: kas meil on piisavalt kaupa ja kus müük toimub?

### 16.1. Loo uus leht

1. All vajuta `+`.
2. Paremklõps lehesakil > `Rename`.
3. Nimi: `C_Operations_Liis`.

### 16.2. Lisa müük kaupluste lõikes

1. Vali `Donut chart` või `Clustered bar chart`.
2. Kui kasutad donut chart'i:
   - `Legend`: `sales[store_location]`.
   - `Values`: `Kogutulu`.
3. Kui kasutad bar chart'i:
   - `Y-axis`: `sales[store_location]`.
   - `X-axis`: `Kogutulu`.
4. Pealkiri: `Müük kaupluste lõikes`.

Soovitus: kui asukohti on rohkem kui 5 või sildid lähevad segaseks, kasuta `Clustered bar chart`, mitte donut chart'i.

### 16.3. Lisa laoseis kategooriate lõikes

1. Vali `Clustered bar chart`.
2. Pane väljadele:
   - `Y-axis`: `products[category]`.
   - `X-axis`: `Laos kokku`.
3. Sorteeri:
   - Visuali `...` > `Sort axis` > `Laos kokku` > `Sort descending`.
4. Pealkiri: `Laoseis kategooriate lõikes`.
5. Värv: `#009B8D`.

### 16.4. Lisa laoriski tabel

1. Vali `Table` visual.
2. Lisa väljad:
   - `products[category]`
   - `inventory[location]`
   - `inventory[quantity_available]`
   - `inventory[reorder_point]`
3. Filtreeri riskikohad:
   - Vali tabel.
   - Paremal `Filters on this visual`.
   - Lohista sinna `inventory[quantity_available]`.
   - Vali `Advanced filtering`.
   - Tingimus: `is less than`.
   - Sisesta käsitsi sobiv piir, näiteks `10`, või kasuta tabelis visuaalselt madalaid väärtusi.

Kui tahad täpsemalt võrrelda `quantity_available < reorder_point`, lisa Power Querys uus veerg:

1. `Home` > `Transform data`.
2. Vali `inventory`.
3. Üleval `Add Column` > `Custom Column`.
4. Uue veeru nimi: `below_reorder_point`.
5. Valem:

```powerquery
[quantity_available] < [reorder_point]
```

6. Vajuta `OK`.
7. `Close & Apply`.
8. Kasuta tabeli filtris `below_reorder_point is True`.

### 16.5. Conditional formatting laoriskile

1. Vali laoriski `Table` visual.
2. Paremal `Visualizations` paneelis, väljade nimekirjas, leia `quantity_available`.
3. Vajuta selle välja kõrval noolekest.
4. Vali `Conditional formatting`.
5. Vali `Background color` või `Font color`.
6. `Format style`: `Rules`.
7. Tee reegel:
   - Kui väärtus on `>= 0` ja `< 10`, värv `#C84C61`.
   - Kui väärtus on `>= 10` ja `< 30`, värv `#D9902F`.
   - Kui väärtus on `>= 30`, värv `#2F8F5B`.
8. Vajuta `OK`.

### 16.6. Liisi äritõlgendus

Lisa `Insert` > `Text box`:

```text
Kaupluste lõikes müük näitab, millised asukohad veavad käivet ja kus võib olla vaja varu ümber jaotada.
Laoseisu vaade näitab, millistes kategooriates või asukohtades on risk, et müüdav kaup saab otsa.
```

## 17. Roll D: Investor dashboard koondvaateks

Investori küsimus: kas UrbanStyle on investeerimisväärne?

### 17.1. Loo uus leht

1. All vajuta `+`.
2. Paremklõps lehesakil > `Rename`.
3. Nimi: `D_Investor_Koond`.

### 17.2. Lisa pealkiri

1. `Insert` > `Text box`.
2. Tekst:

```text
UrbanStyle OÜ - investori dashboard
```

3. Font: 24-30.
4. Värv: `#1A1A2E`.

### 17.3. Lisa 4 KPI kaarti

Lisa ülemisele reale `Card` visualid:

| KPI | Mõõdik |
|---|---|
| Kogutulu | `Kogutulu` |
| Kliendid | `Kliente` |
| Keskmine tellimus | `Keskmine tellimus` |
| Brutomarginaal | `Brutomarginaal %` |

Iga kaardi puhul:

1. Vali `Card`.
2. Lohista mõõdik väljale `Data`.
3. `Format visual` > `General` > `Title`: pane KPI nimi.
4. `Format visual` > `Visual` > `Callout value`: suurenda fonti.

### 17.4. Lisa investori põhiline trend

1. Vali `Line chart`.
2. `X-axis`: `Date[YearMonth]`.
3. `Y-axis`: `Kogutulu`.
4. Pealkiri: `Müügitulu trend`.
5. Joone värv: `#009B8D`.

### 17.5. Lisa turunduse kokkuvõte

1. Vali `Clustered column chart`.
2. `X-axis`: `sales[channel]`.
3. `Y-axis`: `Kogutulu`.
4. Pealkiri: `Käive kanalite lõikes`.

### 17.6. Lisa operatsioonide kokkuvõte

1. Vali `Clustered bar chart`.
2. `Y-axis`: `products[category]`.
3. `X-axis`: `Laos kokku`.
4. Pealkiri: `Laoseis kategooriate lõikes`.

### 17.7. Lisa investori kokkuvõtte tekst

1. `Insert` > `Text box`.
2. Kirjuta 2-3 lauset:

```text
UrbanStyle'i tugevus on kasvav müügitulu, selgelt mõõdetavad müügikanalid ja kategooriapõhine laoseisu ülevaade.
Investori jaoks on peamine küsimus, kas kasv on korratav: selleks tuleb hoida tugevaid kategooriaid laos ja parandada online-kanali väärtust kliendi kohta.
Puuduv andmevajadus: kampaaniakulud ja web_logs allikad, et arvutada täpne ROI.
```

## 18. Lisa annotatsioon ehk "so what?"

Power BI-s lihtne annotatsioon:

1. Vali ülevalt `Insert`.
2. Vali `Text box`.
3. Kirjuta lühike järeldus, näiteks:

```text
Detsembri hüpe võib viidata jõulukampaaniale.
```

4. Paiguta tekst trendijoonise kõrvale.
5. Soovi korral vali `Insert` > `Shapes` > `Arrow`.
6. Suuna nool diagrammi olulisele punktile.
7. Värv: `#D9902F`.

## 19. Kontrollnimekiri enne esitamist

Iga roll kontrollib:

- Dashboard vastab stakeholder'i küsimusele.
- Lehel on vähemalt 2 diagrammi.
- Vähemalt üks diagramm on sorteeritud loogiliselt.
- KPI või diagrammi pealkiri ütleb, mida vaadata.
- Värvid on rahulikud ja järjepidevad.
- 3D efekte ei ole.
- Ekraan mahub ühele lehele.
- Iga diagrammi kohta on 1-2 lauset äritõlgendust.

## 20. Ekraanipildi tegemine

Power BI-st kiire ekraanipilt:

1. Ava valmis raportileht.
2. Vajuta klaviatuuril `Windows` + `Shift` + `S`.
3. Vali ristkülikuga ainult dashboard'i ala.
4. Salvesta pilt kausta:

```text
C:\Users\Kätlin\Documents\Õppeprojekt\daca-portfolio\week-5
```

Failinimed:

```text
week5_roll_a_ceo_dashboard.png
week5_roll_b_marketing_dashboard.png
week5_roll_c_operations_dashboard.png
week5_roll_d_investor_dashboard.png
```

## 21. Google Slides'i koondvaade

Koondslide'i soovituslik ülesehitus:

```text
UrbanStyle OÜ - investori dashboard

[Kogutulu] [Kliendid] [Keskmine tellimus] [Brutomarginaal]

[Müügitulu trend - Roll A]

[Kanalite efektiivsus - Roll B]    [Laoseis / kauplused - Roll C]

Investori kokkuvõte:
UrbanStyle kasvab, kuid kasv vajab tugevat laoplaneerimist ja täpsemat turundusmõõtmist.
```

## 22. Portfoolio README tekst

Lisa `week-5/README.md` faili näiteks:

```markdown
# Nädal 5: GT_Viz_Disain

## Tööriist

Kasutasin Microsoft Power BI Desktop versiooni 2.153.910.0 64-bit (April 2026).

## Minu roll

Minu stakeholder oli [Kristi / Anna / Liis / Investor].

## Dashboard

![Dashboard](week5_roll_x_dashboard.png)

## Äritõlgendus

Esimene diagramm näitab, et ...
Teine diagramm näitab, et ...

## Disainiotsused

Kasutasin [joon/tulp/KPI] diagrammi, sest ...
Värvipalett põhineb UrbanStyle värvidel `#009B8D` ja `#1A1A2E`.
Eemaldasin üleliigsed elemendid, et stakeholder saaks põhisõnumist kiiresti aru.

## AI kasutamine

AI aitas koostada Power BI sammud, valida sobivad diagrammitüübid ja sõnastada äritõlgenduse.
```

## 23. Kui midagi Power BI-s ei klapi

| Probleem | Lahendus |
|---|---|
| Täpitähed on katki | Impordis vali `File Origin` = `65001: Unicode (UTF-8)` |
| Kuupäev ei tööta trendis | Kontrolli Power Querys, et `sale_date` on `Date/Time` |
| Seos ei teki | Kontrolli, et mõlemad ID veerud on `Whole Number` |
| DAX `RELATED` annab vea | Kontrolli, et `products` -> `sales` seos on olemas |
| `Kasv YoY %` on tühi | Andmetes puudub võrdlusperiood või kuupäevaseos on vale |
| Donut chart on segane | Kasuta `Clustered bar chart` |
| Dashboard ei mahu lehele | Vähenda visualide arvu ja jäta ainult KPI + 2 põhidiagrammi |

## 24. Kasutatud Power BI dokumentatsioon

- Microsoft Learn: Get started with Power BI Desktop  
  https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-getting-started
- Microsoft Learn: Data sources in Power BI Desktop  
  https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-data-sources
- Microsoft Learn: Report view in Power BI Desktop  
  https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-format-pane
- Microsoft Learn: Create a card visual in Power BI  
  https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-new-card
- Microsoft Learn: Conditional formatting in Power BI visuals  
  https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-conditional-formatting

