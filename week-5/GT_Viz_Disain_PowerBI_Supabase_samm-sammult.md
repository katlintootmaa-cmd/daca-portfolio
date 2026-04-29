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

## 3. Soovituslik: loo Power BI jaoks vaated Supabase'is

See samm ei ole kohustuslik, aga teeb raporti palju lihtsamaks. Vaated ühendavad vajalikud tabelid juba Supabase poolel.

Tee nii:

1. Ava Supabase Dashboard.
2. Vali UrbanStyle projekt.
3. Vasakult menüüst vali `SQL Editor`.
4. Vajuta `New query`.
5. Kopeeri päringukasti järgmine SQL.
6. Vajuta `Run`.

```sql
create or replace view public.v_powerbi_sales_enriched as
select
    s.sale_id,
    s.invoice_id,
    s.sale_date,
    s.customer_id,
    s.product_id,
    s.quantity,
    s.unit_price,
    s.total_price,
    s.channel,
    coalesce(s.store_location, 'Online') as store_location,
    s.payment_method,
    p.product_name,
    p.category,
    p.subcategory,
    p.supplier,
    p.cost_price,
    p.retail_price,
    p.eco_certified,
    c.city as customer_city,
    c.loyalty_tier,
    c.birth_year
from public.sales s
left join public.products p
    on p.product_id = s.product_id
left join public.customers c
    on c.customer_id = s.customer_id;
```

Kui päring lõppes veata, tee teine vaade.

1. Vajuta uuesti `New query`.
2. Kopeeri päringukasti järgmine SQL.
3. Vajuta `Run`.

```sql
create or replace view public.v_powerbi_inventory_enriched as
select
    i.inventory_id,
    i.product_id,
    i.location,
    i.quantity_available,
    i.reorder_point,
    i.last_updated,
    p.product_name,
    p.category,
    p.subcategory,
    p.supplier,
    p.cost_price,
    p.retail_price,
    case
        when i.quantity_available <= i.reorder_point then true
        else false
    end as needs_reorder
from public.inventory i
left join public.products p
    on p.product_id = i.product_id;
```

Kontrolli kohe, et mõlemad vaated töötavad.

1. Vajuta `New query`.
2. Kopeeri päringukasti kontrollpäringud.
3. Vajuta `Run`.

```sql
select * from public.v_powerbi_sales_enriched limit 10;
select * from public.v_powerbi_inventory_enriched limit 10;
```

Kui mõlemad päringud annavad read tagasi, võid minna Power BI-sse.

## 4. Ava Power BI ja alusta uut faili

1. Ava `Microsoft Power BI Desktop`.
2. Vali `Blank report`.
3. Vajuta vasakul üleval `File`.
4. Vali `Save as`.
5. Salvesta fail kohe:

```text
C:\Users\Kätlin\Documents\Õppeprojekt\daca-portfolio\week-5\gt_viz_disain_urbanstyle_supabase.pbix
```

## 5. Vali tabelid või vaated

Tee seda siis, kui Power BI näitab sulle andmeallika `Navigator` akent või tabelite nimekirja.

1. Leia schema `public`.
2. Kui tegid peatükis 3 Power BI vaated, vali need kaks vaadet:

- `public v_powerbi_sales_enriched`
- `public v_powerbi_inventory_enriched`

3. Kui vaateid ei teinud, vali põhitäbelid:

- `public sales`
- `public customers`
- `public products`
- `public inventory`

4. Vajuta `Transform Data`, mitte kohe `Load`.

Kui tabelite nimekirja ei näe, kontrolli, et oled valinud schema `public`.

## 6. Kontrolli Power Querys andmetüübid

Power Query Editoris kontrolli andmetüübid enne andmete laadimist.

1. Vasakul `Queries` paneelis vali `v_powerbi_sales_enriched`.
2. Vaata iga veeru päises olevat andmetüübi ikooni.
3. Kui tüüp on vale, vajuta veeru päises ikoonile.
4. Vali õige tüüp.
5. Kui Power BI küsib `Replace current step?`, vali `Replace current`.

Kui kasutad vaadet `v_powerbi_sales_enriched`, kontrolli neid tüüpe.

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
| `category` | Text |
| `subcategory` | Text |
| `cost_price` | Decimal Number |
| `retail_price` | Decimal Number |
| `eco_certified` | True/False |
| `customer_city` | Text |
| `loyalty_tier` | Text |
| `birth_year` | Whole Number |

Nüüd vali vasakult `v_powerbi_inventory_enriched` ja kontrolli need tüübid.

| Veerg | Tüüp |
|---|---|
| `inventory_id` | Whole Number |
| `product_id` | Whole Number |
| `location` | Text |
| `quantity_available` | Whole Number |
| `reorder_point` | Whole Number |
| `last_updated` | Date/Time |
| `category` | Text |
| `needs_reorder` | True/False |

### 6.1. Tee Power Query kvaliteedikontroll

Enne `Close & Apply` vajutamist tee väike kontroll. See aitab vältida olukorda, kus dashboard'i ehitamisel otsid viga visualist, kuigi probleem on andmetüübis või päringus.

1. Kontrolli vasakult `Queries` paneelist, et näed õigeid tabeleid või vaateid.
2. Kui kasutad vaateid, peaksid nimekirjas olema:
   - `v_powerbi_sales_enriched`
   - `v_powerbi_inventory_enriched`
3. Kui kasutad põhitäbeleid, peaksid nimekirjas olema:
   - `sales`
   - `customers`
   - `products`
   - `inventory`
4. Vali iga tabel või vaade ükshaaval.
5. Kontrolli, et üheski veerus ei oleks väärtust `Error`.
6. Kontrolli, et ID veerud oleksid `Whole Number`.
7. Kontrolli, et hinna ja käibe veerud oleksid `Decimal Number`.
8. Kontrolli, et kuupäevaveerud oleksid `Date` või `Date/Time`.
9. Kontrolli, et tekstiveerud nagu `category`, `channel`, `location` ja `loyalty_tier` oleksid `Text`.
10. Kui mõnes veerus on tüüp vale, muuda see enne andmete laadimist ära.

Kiirkontroll:

| Kontroll | Mida peab nägema |
|---|---|
| Müügikuupäev | `sale_date` on `Date/Time` |
| Raha | `total_price`, `unit_price`, `cost_price` on `Decimal Number` |
| Kogused | `quantity`, `quantity_available`, `reorder_point` on `Whole Number` |
| Kategooriad | `category`, `subcategory`, `channel` on `Text` |
| Laorisk | `needs_reorder` on `True/False` |

Kui kõik on korras:

1. Vali Power Query Editoris `Home`.
2. Vajuta `Close & Apply`.
3. Oota, kuni Power BI laeb andmed mudelisse.

## 7. Kui kasutad põhitäbeleid, loo seosed

Kui kasutad ainult kahte vaadet, võid selle peatüki vahele jätta.

Kui importisid `sales`, `customers`, `products` ja `inventory` eraldi tabelitena:

1. Mine vasakul `Model view`.
2. Loo või kontrolli seosed:

| Seos | Kardinaalsus | Suund |
|---|---|---|
| `customers[customer_id]` -> `sales[customer_id]` | One-to-many | Single |
| `products[product_id]` -> `sales[product_id]` | One-to-many | Single |
| `products[product_id]` -> `inventory[product_id]` | One-to-many | Single |

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

Kui kasutad vaadet:

1. Mine vasakul `Model view`.
2. Lohista `Date[Date]` veerult seos `v_powerbi_sales_enriched[sale_date]` veerule.
3. Kui Power BI küsib kuupäevaveeru date-osa, vali date-osa.
4. Kontrolli, et seos oleks aktiivne.

Kui Power BI ei lase `Date` ja `Date/Time` veergu ühendada, tee Power Querys müügivaates uus veerg:

1. Vali `v_powerbi_sales_enriched`.
2. Vali `Add Column`.
3. Vali `Date` > `Date Only`.
4. Nimeta uus veerg `sale_day`.
5. Loo seos `Date[Date]` -> `v_powerbi_sales_enriched[sale_day]`.

## 9. Loo põhimõõdikud

Mõõdikud loo ükshaaval. Kui kasutad vaadet `v_powerbi_sales_enriched`, tee nii:

1. Mine `Report view` vaatesse.
2. Paremal `Data` paneelis tee paremklõps tabelil `v_powerbi_sales_enriched`.
3. Vali `New measure`.
4. Kopeeri valemiribale esimene mõõdik.
5. Vajuta `Enter`.
6. Korda sama iga järgmise mõõdikuga.

```DAX
Kogutulu =
SUM ( v_powerbi_sales_enriched[total_price] )
```

```DAX
Müüdud ühikuid =
SUM ( v_powerbi_sales_enriched[quantity] )
```

```DAX
Tellimusi =
DISTINCTCOUNT ( v_powerbi_sales_enriched[invoice_id] )
```

```DAX
Kliente =
DISTINCTCOUNT ( v_powerbi_sales_enriched[customer_id] )
```

```DAX
Keskmine tellimus =
DIVIDE ( [Kogutulu], [Tellimusi] )
```

```DAX
Brutokasum =
SUMX (
    v_powerbi_sales_enriched,
    v_powerbi_sales_enriched[total_price]
        - v_powerbi_sales_enriched[quantity] * v_powerbi_sales_enriched[cost_price]
)
```

```DAX
Brutomarginaal % =
DIVIDE ( [Brutokasum], [Kogutulu] )
```

Laoseisu mõõdikud loo `v_powerbi_inventory_enriched` tabelile.

1. Paremal `Data` paneelis tee paremklõps tabelil `v_powerbi_inventory_enriched`.
2. Vali `New measure`.
3. Lisa järgmised mõõdikud ükshaaval.

```DAX
Laos kokku =
SUM ( v_powerbi_inventory_enriched[quantity_available] )
```

```DAX
Alla tellimispunkti tooteid =
CALCULATE (
    COUNTROWS ( v_powerbi_inventory_enriched ),
    v_powerbi_inventory_enriched[needs_reorder] = TRUE ()
)
```

Kui kasutad eraldi põhitäbeleid, asenda mõõdikutes tabelinimi vastavalt:

- `v_powerbi_sales_enriched` -> `sales`
- `v_powerbi_inventory_enriched` -> `inventory`

Brutokasumi puhul on eraldi tabelite mudelis vaja töötavat seost `products` -> `sales` ja valemit:

```DAX
Brutokasum =
SUMX (
    sales,
    sales[total_price] - sales[quantity] * RELATED ( products[cost_price] )
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

Kontrolli enne esitamist:

- Pealkiri ütleb, mida visual näitab.
- Teljed ja sildid on loetavad.
- 3D efekte ei ole.
- Ühel lehel ei ole liiga palju visuale.
- Kõik numbrid on vormindatud loogiliselt.
- Iga visual vastab stakeholder'i küsimusele.

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
