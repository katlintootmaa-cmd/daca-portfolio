# GT_Viz_Disain grupitöö: Power BI + Supabase samm-sammult juhend

Versioon: Microsoft Power BI Desktop 2.153.910.0 64-bit, April 2026  
Töö: DACA nädal 5, visualiseerimise disain, grupitöö  
Andmeallikas: UrbanStyle andmed Supabase Postgres andmebaasis

## 1. Eesmärk

Selle juhendi eesmärk on teha UrbanStyle andmetest Power BI raport nii, et andmed tulevad otse Supabase andmebaasist, mitte CSV failidest.

Juhend eeldab, et Power BI ja Supabase vaheline andmeallikas on sul juba olemas või õpetaja on selle ette valmistanud. Siin failis ei ole ühenduse loomise juhiseid, vaid töö algab andmete ettevalmistamisest ja raporti ehitamisest.

See sobib eriti hästi siis, kui tahad grupitöös näidata realistlikumat andmevoogu:

```text
Supabase Postgres -> Power BI Desktop -> dashboard -> ekraanipilt / portfoolio
```

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

## 2. Mida vajad enne alustamist

Sul peab olema:

- Supabase projekt, kus UrbanStyle tabelid on juba olemas.
- Microsoft Power BI Desktop.
- Ligipääs Supabase Dashboardile.

UrbanStyle põhitäbelid:

| Tabel | Milleks kasutatakse |
|---|---|
| `products` | toodete kategooriad, hinnad, tarnijad |
| `customers` | kliendid, linnad, lojaalsustase |
| `sales` | müügitehingud |
| `inventory` | laoseis asukohtade lõikes |

Bonus-tabelid, kui tahad rohkem analüüsi:

| Tabel | Milleks kasutatakse |
|---|---|
| `web_logs` | veebikäitumine ja kanalid |
| `inventory_movements` | laokannete ajalugu |
| `suppliers` | tarnijate info |
| `promotions` | kampaaniad |

## 3. Kontrolli Supabase'is tabelid üle

Enne Power BI-sse minekut kontrolli, et Supabase'is on olemas õiged UrbanStyle tabelid.

Tee nii:

1. Ava Supabase Dashboard.
2. Vali UrbanStyle projekt.
3. Vasakult menüüst vali `SQL Editor`.
4. Vajuta `New query`.
5. Kopeeri päringukasti järgmine kontrollpäring.
6. Vajuta `Run`.

```sql
select table_name
from information_schema.tables
where table_schema = 'public'
  and table_name in (
      'customers',
      'inventory',
      'inventory_movements',
      'products',
      'promotions',
      'sales',
      'suppliers',
      'web_logs'
  )
order by table_name;
```

Kui päring tagastab need tabelid, võid minna Power BI-sse.

## 4. Ava Power BI ja alusta uut faili

1. Ava `Microsoft Power BI Desktop`.
2. Vali `Blank report`.
3. Vajuta vasakul üleval `File`.
4. Vali `Save as`.
5. Salvesta fail kohe:

```text
C:\Users\Kätlin\Documents\Õppeprojekt\daca-portfolio\week-5\gt_viz_disain_urbanstyle_supabase.pbix
```

## 5. Vali tabelid

Tee seda siis, kui Power BI näitab sulle andmeallika `Navigator` akent või tabelite nimekirja.

1. Leia schema `public`.
2. Vali Supabase'i tabelid:

- `public customers`
- `public inventory`
- `public inventory_movements`
- `public products`
- `public promotions`
- `public sales`
- `public suppliers`
- `public web_logs`

Ära vali `public customers_test` tabelit. See on test- või puhastustabel, mitte raporti põhiandmestik.

3. Vajuta `Transform Data`, mitte kohe `Load`.

Kui tabelite nimekirja ei näe, kontrolli, et oled valinud schema `public`.

## 6. Kontrolli Power Querys andmetüübid

Power Query Editoris kontrolli andmetüübid enne andmete laadimist.

1. Vasakul `Queries` paneelis vali `sales`.
2. Vaata iga veeru päises olevat andmetüübi ikooni.
3. Kui tüüp on vale, vajuta veeru päises ikoonile.
4. Vali õige tüüp.
5. Kui Power BI küsib `Replace current step?`, vali `Replace current`.

`sales` tabelis kontrolli neid tüüpe.

| Veerg | Tüüp Power BI-s |
|---|---|
| `sale_id` | Whole Number |
| `invoice_id` | Text |
| `sale_date` | Date/Time |
| `customer_id` | Whole Number |
| `product_id` | Whole Number |
| `quantity` | Whole Number |
| `unit_price` | Decimal Number |
| `total_price` | Decimal Number |
| `channel` | Text |
| `store_location` | Text |
| `payment_method` | Text |

Nüüd vali vasakult `products` ja kontrolli need tüübid.

| Veerg | Tüüp |
|---|---|
| `product_id` | Whole Number |
| `product_name` | Text |
| `category` | Text |
| `subcategory` | Text |
| `supplier` | Text |
| `cost_price` | Decimal Number |
| `retail_price` | Decimal Number |
| `eco_certified` | True/False |

Nüüd vali vasakult `customers` ja kontrolli need tüübid.

| Veerg | Tüüp |
|---|---|
| `customer_id` | Whole Number |
| `city` | Text |
| `loyalty_tier` | Text |
| `birth_year` | Whole Number |

Nüüd vali vasakult `inventory` ja kontrolli need tüübid.

| Veerg | Tüüp |
|---|---|
| `inventory_id` | Whole Number |
| `product_id` | Whole Number |
| `location` | Text |
| `quantity_available` | Whole Number |
| `reorder_point` | Whole Number |
| `last_updated` | Date/Time |

### 6.1. Puhasta ja ühtlusta andmed Power Querys

Need sammud tulevad samast loogikast nagu CSV põhises Power BI juhendis, aga siin teed need Supabase'ist imporditud tabelitele Power Query Editoris.

#### 6.1.1. Puhasta `sales`

1. Vali vasakult `sales`.
2. Vali veerg `total_price`.
3. Üleval vali `Home` > `Remove Rows` > `Remove Errors`, kui veerus on vigu.
4. Vali veerg `sale_date`.
5. Vali uuesti `Home` > `Remove Rows` > `Remove Errors`, kui kuupäevades on vigu.

Kui tahad tagastused või negatiivsed müügiread raportist välja jätta:

1. Vali veeru `total_price` päises filtrinool.
2. Vali `Number Filters`.
3. Vali `Greater Than...`.
4. Sisesta `0`.
5. Vajuta `OK`.

Grupitöö jaoks on lihtsam kasutada ainult positiivseid müüke. Kui tahad tagastusi analüüsida, ära seda filtrit rakenda.

#### 6.1.2. Ühtlusta `sales[store_location]`

1. Vali `sales` tabelis veerg `store_location`.
2. Üleval vali `Transform`.
3. Vajuta `Format` > `Trim`.
4. Vajuta `Format` > `Clean`.

Online müükidel võib `store_location` olla tühi. Selle parandamiseks:

1. Vali veerg `store_location`.
2. Üleval vali `Transform`.
3. Vajuta `Replace Values`.
4. `Value To Find`: jäta tühjaks.
5. `Replace With`: kirjuta `Online`.
6. Vajuta `OK`.

Kui tühja väärtuse asendamine nii ei toimi, jäta see samm vahele ja kasuta raportis `sales[channel]` filtrit online müügi eristamiseks.

#### 6.1.3. Ühtlusta `customers[city]`

1. Vali vasakult `customers`.
2. Vali veerg `city`.
3. Üleval vali `Transform`.
4. Vajuta `Format` > `Trim`.
5. Vajuta `Format` > `Clean`.

Kui linnade kirjapilt on ebaühtlane, paranda sagedasemad variandid käsitsi:

1. Vali veerg `city`.
2. Vali `Transform` > `Replace Values`.
3. Asenda näiteks `Tallinn ` väärtusega `Tallinn`.
4. Korda sama teiste nähtavate kirjavigade või tühikutega.

#### 6.1.4. Ühtlusta tekstiveerud `products` ja `inventory` tabelites

Tee sama `Trim` ja `Clean` samm ka nendele veergudele:

- `products[category]`
- `products[subcategory]`
- `products[supplier]`
- `inventory[location]`

See aitab vältida olukorda, kus Power BI näitab sama kategooriat või asukohta mitme eraldi väärtusena ainult peidetud tühiku tõttu.

#### 6.1.5. Kui tekib `Errors in customers`

Kui vasakul tekib grupp `Query Errors` ja selle all `Errors in customers`, ära kasuta seda põhitabelina. See on Power BI loodud abipäring, mis näitab ainult vigaseid ridu.

Tee nii:

1. Vali vasakult päring `customers`, mitte `Errors in customers`.
2. Paremal `Query Settings` paneelis leia `Applied Steps`.
3. Klõpsa sammul `Changed Type`.
4. Vaata eelvaates, millise veeru päises on `Error`.
5. Kui error on näiteks veerus `phone` või `email`, vali see veerg.
6. Vajuta veeru päises andmetüübi ikoonile.
7. Vali `Text`.
8. Kui Power BI küsib `Replace current step?`, vali `Replace current`.

`customers` tabelis peaksid tekstina olema vähemalt `first_name`, `last_name`, `email`, `phone`, `city` ja `loyalty_tier`.

Kui `Errors in customers` jääb pärast parandust ikka vasakule:

1. Tee vasakul `Errors in customers` päringul paremklõps.
2. Vali `Delete`.
3. Kui Power BI küsib kinnitust, vajuta `Delete`.

Kui `Close & Apply` annab ikka vea, vali `customers` tabelis `Home` > `Remove Rows` > `Remove Errors`. Tee seda ainult siis, kui vigaseid ridu on vähe ja sul on vaja raport kiiresti valmis saada.

### 6.2. Tee Power Query kvaliteedikontroll

Enne `Close & Apply` vajutamist tee väike kontroll. See aitab vältida olukorda, kus dashboard'i ehitamisel otsid viga visualist, kuigi probleem on andmetüübis või päringus.

1. Kontrolli vasakult `Queries` paneelist, et näed õigeid tabeleid.
2. Nimekirjas peaksid olema:
   - `customers`
   - `inventory`
   - `inventory_movements`
   - `products`
   - `promotions`
   - `sales`
   - `suppliers`
   - `web_logs`
   - `customers_test` ei tohi olla valitud
3. Vali iga tabel ükshaaval.
4. Kontrolli, et üheski veerus ei oleks väärtust `Error`.
5. Kontrolli, et ID veerud oleksid `Whole Number`.
6. Kontrolli, et hinna ja käibe veerud oleksid `Decimal Number`.
7. Kontrolli, et kuupäevaveerud oleksid `Date` või `Date/Time`.
8. Kontrolli, et tekstiveerud nagu `category`, `channel`, `location` ja `loyalty_tier` oleksid `Text`.
9. Kui mõnes veerus on tüüp vale, muuda see enne andmete laadimist ära.

Kiirkontroll:

| Kontroll | Mida peab nägema |
|---|---|
| Müügikuupäev | `sale_date` on `Date/Time` |
| Raha | `sales[total_price]`, `sales[unit_price]` ja `products[cost_price]` on `Decimal Number` |
| Kogused | `quantity`, `quantity_available`, `reorder_point` on `Whole Number` |
| Kategooriad | `products[category]`, `products[subcategory]` ja `sales[channel]` on `Text` |
| Laorisk | `inventory[quantity_available]` ja `inventory[reorder_point]` on numbrilised |

Kui kõik on korras:

1. Vali Power Query Editoris `Home`.
2. Vajuta `Close & Apply`.
3. Oota, kuni Power BI laeb andmed mudelisse.

## 7. Loo tabelite seosed

Kui importisid Supabase'i tabelid Power BI-sse:

1. Mine vasakul `Model view`.
2. Loo või kontrolli seosed:

| Seos | Kardinaalsus | Suund |
|---|---|---|
| `customers[customer_id]` -> `sales[customer_id]` | One-to-many | Single |
| `products[product_id]` -> `sales[product_id]` | One-to-many | Single |
| `products[product_id]` -> `inventory[product_id]` | One-to-many | Single |
| `products[product_id]` -> `inventory_movements[product_id]` | One-to-many | Single |
| `suppliers[supplier_name]` -> `products[supplier]` | One-to-many | Single |

Kui Power BI pakub many-to-many seost, kontrolli, kas ID veerud on õige tüübiga.

## 8. Loo kuupäevatabel

Kuupäevatabel on vajalik, et müügitulu trend ja ajafiltrid töötaksid korrektselt.

1. Mine Power BI-s `Report view` vaatesse.
2. Üleval ribal vali `Modeling`.
3. Vajuta `New table`.
4. Sisesta valemiribale järgmine DAX.
5. Vajuta `Enter`.

```DAX
Date =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2023, 1, 1 ), DATE ( 2025, 2, 28 ) ),
    "Year", YEAR ( [Date] ),
    "Month", FORMAT ( [Date], "MMM" ),
    "YearMonth", FORMAT ( [Date], "YYYY-MM" )
)
```

Seo kuupäevatabel müügitabeliga.

1. Mine vasakul `Model view`.
2. Lohista `Date[Date]` veerult seos `sales[sale_date]` veerule.
3. Kui Power BI küsib kuupäevaveeru date-osa, vali date-osa.
4. Kontrolli, et seos oleks aktiivne.

Kui Power BI ei lase `Date` ja `Date/Time` veergu ühendada, tee Power Querys müügitabelisse uus veerg:

1. Vali `sales`.
2. Vali `Add Column`.
3. Vali `Date` > `Date Only`.
4. Nimeta uus veerg `sale_day`.
5. Loo seos `Date[Date]` -> `sales[sale_day]`.

## 9. Loo põhimõõdikud

Mõõdikud loo ükshaaval `sales` tabelile.

1. Mine `Report view` vaatesse.
2. Paremal `Data` paneelis tee paremklõps tabelil `sales`.
3. Vali `New measure`.
4. Kopeeri valemiribale esimene mõõdik.
5. Vajuta `Enter`.
6. Korda sama iga järgmise mõõdikuga.

```DAX
Kogutulu =
SUM ( sales[total_price] )
```

```DAX
Müüdud ühikuid =
SUM ( sales[quantity] )
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
DIVIDE ( [Kogutulu], [Tellimusi] )
```

```DAX
Brutokasum =
SUMX (
    sales,
    sales[total_price] - sales[quantity] * RELATED ( products[cost_price] )
)
```

```DAX
Brutomarginaal % =
DIVIDE ( [Brutokasum], [Kogutulu] )
```

Laoseisu mõõdikud loo `inventory` tabelile.

1. Paremal `Data` paneelis tee paremklõps tabelil `inventory`.
2. Vali `New measure`.
3. Lisa järgmised mõõdikud ükshaaval.

```DAX
Laos kokku =
SUM ( inventory[quantity_available] )
```

```DAX
Alla tellimispunkti tooteid =
CALCULATE (
    COUNTROWS ( inventory ),
    inventory[quantity_available] <= inventory[reorder_point]
)
```

### 9.1. Tee mõõdikute testleht

Enne päris stakeholder'i dashboard'ide tegemist tee üks ajutine testleht. See aitab kontrollida, kas mõõdikud, seosed ja kuupäevad töötavad.

1. All lehesakkide juures vajuta `+`, et luua uus raportileht.
2. Tee lehe nimel paremklõps.
3. Vali `Rename`.
4. Nimeta leht `Test`.
5. Lisa `Card` visual ja pane väärtuseks `Kogutulu`.
6. Lisa teine `Card` visual ja pane väärtuseks `Tellimusi`.
7. Lisa kolmas `Card` visual ja pane väärtuseks `Kliente`.
8. Lisa `Table` visual.
9. Pane tabelisse `category` ja `Kogutulu`.
10. Lisa `Line chart`.
11. Pane X-teljeks `Date[YearMonth]` ja Y-väärtuseks `Kogutulu`.
12. Lisa `Slicer` visual.
13. Pane slicerisse `category`.
14. Vali sliceris üks kategooria ja kontrolli, kas kaardid ning joondiagramm muutuvad.

Kui slicer muudab numbreid, töötavad seosed ja mõõdikud tõenäoliselt õigesti.

Kui midagi tundub vale:

| Probleem | Kontrolli |
|---|---|
| `Kogutulu` on tühi | Kas `total_price` on `Decimal Number` ja tabelis on read olemas |
| `Tellimusi` on tühi | Kas `invoice_id` on olemas ja `Text` tüübiga |
| Joondiagramm on tühi | Kas `Date` tabel on seotud müügikuupäevaga |
| Slicer ei muuda numbreid | Kas mudelis on aktiivsed seosed |
| Kategooriad ei ilmu | Kas `category` on imporditud ja `Text` tüübiga |

## 10. Vorminda mõõdikud

Vorminda mõõdikud kohe pärast loomist.

1. Paremal `Data` paneelis klõpsa mõõdikul.
2. Üleval avaneb `Measure tools` või `Measure`.
3. Vali sobiv `Format`.
4. Vajadusel määra `Decimal places` väärtuseks `0` või `2`.
5. Korda sama kõigi mõõdikutega.

| Mõõdik | Formaat |
|---|---|
| `Kogutulu` | Currency või Decimal number |
| `Keskmine tellimus` | Currency või Decimal number |
| `Brutokasum` | Currency või Decimal number |
| `Brutomarginaal %` | Percentage |
| `Müüdud ühikuid` | Whole number |
| `Tellimusi` | Whole number |
| `Kliente` | Whole number |
| `Laos kokku` | Whole number |

Kui euro sümbol ei tööta mugavalt, pane ühik visuali pealkirja, näiteks `Kogutulu (EUR)`.

### 10.1. Rakenda ühtne kujundus enne rollivaadete tegemist

Et kõigi grupiliikmete dashboard'id näeksid välja sama stiiliga, leppige enne rollivaadete tegemist kokku üks kujundus ja kasutage seda igal lehel.

Kasuta kõigil Power BI lehtedel sama põhistiili:

| Element | Seadistus |
|---|---|
| Page background | `#F7F9FB` või valge |
| Visual background | valge |
| Põhivärv | `#009B8D` |
| Tume tekst | `#1A1A2E` |
| Rõhuvärv / hoiatus | `#D9902F` |
| Font | Segoe UI |
| Pealkirja suurus | 14-16 pt |
| Telgede ja siltide suurus | 10-11 pt |
| Kaardi numbri suurus | 24-32 pt |

Tee iga visuali puhul sama vormindus:

1. Klõpsa visualil.
2. Ava paremal `Format visual`.
3. `General` > `Title`: lülita sisse.
4. Määra pealkirja fondiks `Segoe UI`.
5. Määra pealkirja värviks `#1A1A2E`.
6. Määra diagrammi põhivärviks `#009B8D`.
7. Kui visual vajab hoiatust või rõhutust, kasuta ainult värvi `#D9902F`.
8. Hoia taust valge või väga helehall.
9. Ära kasuta 3D efekte, varjusid ega juhuslikke lisavärve.

Kaartide puhul kasuta sama stiili:

| Kaardi osa | Seadistus |
|---|---|
| Category label | sees, `#1A1A2E`, Segoe UI |
| Callout value | `#009B8D`, Segoe UI, suur ja loetav |
| Background | valge |
| Border | helehall või välja lülitatud |

Diagrammide puhul kasuta sama stiili:

| Diagrammi osa | Seadistus |
|---|---|
| Data colors | esimene värv `#009B8D` |
| X-axis ja Y-axis | tekst `#1A1A2E`, Segoe UI |
| Data labels | sisse ainult siis, kui need ei tee visuali kirjuks |
| Legend | sees ainult siis, kui visualis on mitu sarja |

## 11. Roll A: CEO dashboard

CEO põhiküsimus: kas UrbanStyle kasvab?

Tee CEO leht nii:

1. All lehesakkide juures vajuta `+`, et luua uus raportileht.
2. Tee lehe nimel paremklõps.
3. Vali `Rename`.
4. Nimeta leht `CEO`.
5. Lisa esimene `Card` visual ja pane väärtuseks `Kogutulu`.
6. Lisa teine `Card` visual ja pane väärtuseks `Tellimusi`.
7. Lisa `Line chart`.
8. Pane X-teljeks `Date[YearMonth]` ja Y-väärtuseks `Kogutulu`.
9. Lisa `Clustered column chart`.
10. Pane X-teljeks `category` ja Y-väärtuseks `Kogutulu`.
11. Muuda visualide pealkirjad allolevate soovituste järgi.
12. Rakenda kõigile visualidele samad värvid ja font jaotisest 10.1.

Soovituslikud visualid:

| Visual | Väljad |
|---|---|
| Card | `Kogutulu` |
| Card | `Tellimusi` |
| Line chart | X: `Date[YearMonth]`, Y: `Kogutulu` |
| Clustered column chart | X: `category`, Y: `Kogutulu` |

Pealkirjad:

- `Kogutulu perioodil`
- `Müügitulu trend`
- `Käive kategooriate lõikes`

Äritõlgenduse näide:

```text
Müügitulu trend näitab, kas UrbanStyle'i kasv on järjepidev või sõltub üksikutest müügikuudest.
Kategooriate võrdlus aitab CEO-l näha, millised tooterühmad kasvu kõige rohkem veavad.
```

Mida edastada rollile D:

1. Tee CEO lehelt ekraanipilt.
2. Kirjuta D-le 1-2 lauset kasvu kohta.
3. Too välja, kas müügitulu trend on pigem kasvav, langev või kõikuv.
4. Too välja, milline kategooria annab kõige rohkem käivet.

Näidis D-le saatmiseks:

```text
CEO vaade: müügitulu trend on [kasvav / langev / kõikuv].
Kõige suurema käibega kategooria on [kategooria].
Investorivaates saab seda kasutada kasvu tugevuse hindamiseks.
```

## 12. Roll B: Marketing dashboard

Marketingi põhiküsimus: kas müügikanalid töötavad?

Tee Marketingi leht nii:

1. Loo uus raportileht.
2. Nimeta leht `Marketing`.
3. Lisa `Clustered column chart`.
4. Pane X-teljeks `channel` ja Y-väärtuseks `Kogutulu`.
5. Lisa `Bar chart`.
6. Pane Y-teljeks `payment_method` ja X-väärtuseks `Tellimusi`.
7. Lisa `Matrix`.
8. Pane ridadeks `loyalty_tier`.
9. Pane veergudeks `channel`.
10. Pane väärtuseks `Kogutulu`.
11. Lisa `Card` visual ja pane väärtuseks `Keskmine tellimus`.
12. Muuda visualide pealkirjad allolevate soovituste järgi.
13. Rakenda kõigile visualidele samad värvid ja font jaotisest 10.1.

Soovituslikud visualid:

| Visual | Väljad |
|---|---|
| Clustered column chart | X: `channel`, Y: `Kogutulu` |
| Bar chart | Y: `payment_method`, X: `Tellimusi` |
| Matrix | Rows: `loyalty_tier`, Columns: `channel`, Values: `Kogutulu` |
| Card | `Keskmine tellimus` |

Pealkirjad:

- `Käive kanalite lõikes`
- `Tellimused makseviisi järgi`
- `Lojaalsustase ja kanal`

Äritõlgenduse näide:

```text
Kanali vaade näitab, kas online või pood toob suurema osa käibest.
Lojaalsustaseme võrdlus aitab hinnata, kas väärtuslikumad kliendid ostavad kindlas kanalis.
```

Mida edastada rollile D:

1. Tee Marketingi lehelt ekraanipilt.
2. Kirjuta D-le 1-2 lauset kanalite toimivuse kohta.
3. Too välja, milline müügikanal annab kõige rohkem käivet.
4. Too välja, kas mõni lojaalsustase või makseviis paistab eriti tugevalt silma.

Näidis D-le saatmiseks:

```text
Marketingi vaade: kõige tugevam kanal on [kanal].
Kõige väärtuslikum kliendigrupp või lojaalsustase on [lojaalsustase], sest [põhjus].
Investorivaates saab seda kasutada müügikanalite skaleeritavuse hindamiseks.
```

## 13. Roll C: Operations dashboard

Operationsi põhiküsimus: kas laoseis ja poed toimivad?

Tee Operationsi leht nii:

1. Loo uus raportileht.
2. Nimeta leht `Operations`.
3. Lisa `Card` visual ja pane väärtuseks `Laos kokku`.
4. Lisa teine `Card` visual ja pane väärtuseks `Alla tellimispunkti tooteid`.
5. Lisa `Clustered bar chart`.
6. Pane Y-teljeks `category` ja X-väärtuseks `Laos kokku`.
7. Lisa `Matrix`.
8. Pane ridadeks `location`.
9. Pane veergudeks `category`.
10. Pane väärtuseks `Laos kokku`.
11. Muuda visualide pealkirjad allolevate soovituste järgi.
12. Rakenda kõigile visualidele samad värvid ja font jaotisest 10.1.

Soovituslikud visualid:

| Visual | Väljad |
|---|---|
| Card | `Laos kokku` |
| Card | `Alla tellimispunkti tooteid` |
| Clustered bar chart | Y: `category`, X: `Laos kokku` |
| Matrix | Rows: `location`, Columns: `category`, Values: `Laos kokku` |

Pealkirjad:

- `Laos kokku`
- `Täiendamist vajavad laokirjed`
- `Laoseis kategooriate lõikes`
- `Laoseis asukohtade ja kategooriate järgi`

Äritõlgenduse näide:

```text
Laoseisu vaade näitab, millistes kategooriates võib tekkida puudujääk.
Asukohapõhine matrix aitab otsustada, kuhu kaupa ümber jaotada või juurde tellida.
```

Mida edastada rollile D:

1. Tee Operationsi lehelt ekraanipilt.
2. Kirjuta D-le 1-2 lauset laoseisu ja riskide kohta.
3. Too välja, mitu toodet või laokirjet on alla tellimispunkti.
4. Too välja, kas laoseis toetab müügikasvu või võib kasvu piirata.

Näidis D-le saatmiseks:

```text
Operationsi vaade: alla tellimispunkti on [arv] laokirjet.
Suurim laorisk on kategoorias [kategooria] või asukohas [asukoht].
Investorivaates saab seda kasutada tegevusriski hindamiseks.
```

## 14. Roll D: Investor dashboard

Investori põhiküsimus: kas UrbanStyle on investeerimisväärne?

Tee Investori leht nii:

1. Loo uus raportileht.
2. Nimeta leht `Investor`.
3. Lisa `Card` visual ja pane väärtuseks `Kogutulu`.
4. Lisa teine `Card` visual ja pane väärtuseks `Brutomarginaal %`.
5. Lisa kolmas `Card` visual ja pane väärtuseks `Kliente`.
6. Lisa `Line chart`.
7. Pane X-teljeks `Date[YearMonth]` ja Y-väärtuseks `Kogutulu`.
8. Lisa `Clustered column chart`.
9. Pane X-teljeks `category` ja Y-väärtuseks `Brutokasum`.
10. Muuda visualide pealkirjad allolevate soovituste järgi.
11. Rakenda kõigile visualidele samad värvid ja font jaotisest 10.1.

Soovituslikud visualid:

| Visual | Väljad |
|---|---|
| Card | `Kogutulu` |
| Card | `Brutomarginaal %` |
| Card | `Kliente` |
| Line chart | X: `Date[YearMonth]`, Y: `Kogutulu` |
| Clustered column chart | X: `category`, Y: `Brutokasum` |

Pealkirjad:

- `Kogutulu`
- `Brutomarginaal`
- `Klientide arv`
- `Müügitulu trend`
- `Brutokasum kategooriate lõikes`

Äritõlgenduse näide:

```text
Investorile on oluline mitte ainult käibe kasv, vaid ka kasumlikkus.
Kui kogutulu kasvab ja brutomarginaal püsib tugev, on UrbanStyle'i ärimudel atraktiivsem.
```

Kuidas D kasutab teiste alaülesannete tulemusi:

1. Kogu A-lt CEO ekraanipilt ja 1-2 kasvujäreldust.
2. Kogu B-lt Marketingi ekraanipilt ja 1-2 kanalite järeldust.
3. Kogu C-lt Operationsi ekraanipilt ja 1-2 laoseisu või riski järeldust.
4. Lisa enda Investori lehele või Google Slides'i kokkuvõttesse lühike koondjäreldus.
5. Koondjärelduses vasta küsimusele: kas UrbanStyle on investeerimisväärne?

D koondteksti näidis:

```text
CEO vaade näitab, et müügitulu on [kasvav / langev / kõikuv].
Marketingi vaade näitab, et tugevaim kanal on [kanal].
Operationsi vaade näitab, et peamine risk on [laorisk / puudub suur laorisk].
Investori vaates tähendab see, et UrbanStyle on [atraktiivne / vajab enne investeeringut parandusi], sest [põhjendus].
```

## 15. Kirjuta äritõlgendus samm-sammult

Iga dashboard'i juurde lisa 1-2 lauset, mis ei kirjelda ainult graafikut, vaid ütleb ka, mida see äri jaoks tähendab.

Tee nii:

1. Vali üks visual.
2. Vaata, mis on seal kõige suurem, väiksem või selgem muutus.
3. Kirjuta esimene lause faktina.
4. Kirjuta teine lause ärilise tähendusena.
5. Kontrolli, et lause vastaks sinu stakeholder'i küsimusele.

Kasuta seda vormi:

```text
Diagramm näitab, et [mis on suurim, väikseim või muutub ajas].
See on [stakeholder] jaoks oluline, sest [äriline põhjus].
```

Näited:

```text
Käive on kõige suurem online-kanalis.
Marketingi jaoks tähendab see, et online-kanalisse tasub panna rohkem kampaaniaeelarvet või testida seal uusi pakkumisi.
```

```text
Mõnes kategoorias on laoseis madal ja tooted on alla tellimispunkti.
Operationsi jaoks tähendab see, et neid kategooriaid tuleb enne järgmist müügiperioodi juurde tellida.
```

```text
Brutomarginaal püsib tugev ka siis, kui müügitulu kasvab.
Investori jaoks tähendab see, et kasv ei tule ainult suurema mahu arvelt, vaid äri võib olla ka kasumlik.
```

Väldi selliseid lauseid:

```text
Siin on tulpdiagramm.
Diagramm näitab müüki.
Numbrid on erinevad.
```

Parem on öelda, mida otsustaja sellest teada saab.

## 16. Disainisoovitused

Kasuta rahulikku ja ühtset visuaalset stiili:

| Element | Soovitus |
|---|---|
| Põhivärv | `#009B8D` |
| Tume tekst | `#1A1A2E` |
| Hoiatus / rõhutus | `#D9902F` |
| Taust | valge või väga helehall |
| Font | Segoe UI |
| Pealkirjad | `#1A1A2E`, 14-16 pt |
| Kaardi väärtused | `#009B8D`, 24-32 pt |
| Teljed ja sildid | `#1A1A2E`, 10-11 pt |

Kontrolli enne esitamist:

- Pealkiri ütleb, mida visual näitab.
- Teljed ja sildid on loetavad.
- 3D efekte ei ole.
- Ühel lehel ei ole liiga palju visuale.
- Kõik numbrid on vormindatud loogiliselt.
- Iga visual vastab stakeholder'i küsimusele.
- Kõigil lehtedel on sama font.
- Kõigil lehtedel on sama värvipalett.
- Kaardid, diagrammid ja matrix'id kasutavad sama tausta ja tekstivärvi.

## 17. Andmete värskendamine

Power BI Desktopis:

1. Vajuta üleval `Home`.
2. Vajuta `Refresh`.
3. Oota, kuni andmed uuenevad.

Kui Supabase tabelites on andmed muutunud, peaksid ka Power BI visualid pärast refresh'i muutuma.

## 18. Ekraanipildi tegemine

Power BI-st kiire ekraanipilt:

1. Ava valmis raportileht.
2. Vajuta `Windows` + `Shift` + `S`.
3. Vali ainult dashboard'i ala.
4. Salvesta pilt kausta:

```text
C:\Users\Kätlin\Documents\Õppeprojekt\daca-portfolio\week-5
```

Failinimed:

```text
week5_supabase_roll_a_ceo_dashboard.png
week5_supabase_roll_b_marketing_dashboard.png
week5_supabase_roll_c_operations_dashboard.png
week5_supabase_roll_d_investor_dashboard.png
```

## 19. Google Slides'i koondvaade

Koondslide'i soovituslik ülesehitus:

```text
UrbanStyle OÜ - Power BI dashboard Supabase andmebaasist

[Kogutulu] [Kliente] [Keskmine tellimus] [Brutomarginaal]

[Müügitulu trend - CEO vaade]

[Kanalite efektiivsus - Marketing]    [Laoseis - Operations]

Investor kokkuvõte:
UrbanStyle'i andmed tulevad Supabase Postgres andmebaasist.
Dashboard näitab kasvu, kanalite toimivust, laoseisu ja kasumlikkust.
```

## 20. Portfoolio README tekst

Lisa `week-5/README.md` faili näiteks:

```markdown
# Nädal 5: GT_Viz_Disain Power BI + Supabase

## Tööriistad

Kasutasin Microsoft Power BI Desktopi ja Supabase Postgres andmebaasi.

## Minu roll

Minu stakeholder oli [Kristi / Anna / Liis / Investor].

## Dashboard

![Dashboard](week5_supabase_roll_x_dashboard.png)

## Äritõlgendus

Esimene diagramm näitab, et ...
Teine diagramm näitab, et ...

## Disainiotsused

Kasutasin [joon/tulp/KPI] diagrammi, sest ...
Värvipalett põhineb UrbanStyle värvidel `#009B8D` ja `#1A1A2E`.

## AI kasutamine

AI aitas koostada Power BI mõõdikud ja dashboard'i struktuuri.
```

## 21. Kui midagi ei tööta

| Probleem | Lahendus |
|---|---|
| Power BI ei näita tabeleid | Kontrolli, et valid schema `public` |
| Vaade ei ilmu Power BI-s | Vajuta `Refresh Preview` |
| Kuupäevatrend ei tööta | Tee Power Querys `sale_day` veerg tüübiga Date |
| Seos ei teki | Kontrolli, et mõlemad ID veerud on `Whole Number` |
| `RELATED` annab vea | Kontrolli, et `products` -> `sales` seos on olemas |
| Numbrid on tekstina | Muuda Power Querys veeru tüüp Decimal Number või Whole Number |
