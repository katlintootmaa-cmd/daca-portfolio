# Peatükk 1: tehniliste oskuste hindamine

## Eesmärk

Esimese peatüki ülesanne on koostada juhend Toomas Kasele, kes on UrbanStyle'i IT-direktor. Tema tahab teada, kuidas hinnata, kas kandidaat oskab päriselt andmetega töötada või on ta ainult CV-sse tööriistade nimed kirjutanud.

## Rollide vaade ja töö selles peatükis

- Palkamisjuht vaatab, millised tehnilised oskused peavad olema CV-s ja kandideerimismaterjalides tõendatud.
- Tehniline intervjueerija koostab SQL-i ja Pythoniga praktilise testi ning hindab lahenduse kvaliteeti.
- Personalijuht jälgib, kuidas kandidaat probleemi lahendades suhtleb, küsib ja oma mõttekäiku selgitab.
- Tiimijuht hindab, kas kandidaadi töö oleks tiimis kasutatav: loetav, dokumenteeritud ja teistele arusaadav.

## Töökäik

Selles peatükis alustasime sellest, et panime kirja, milliseid tehnilisi oskusi UrbanStyle'i andmeanalüütik oma igapäevatöös kasutaks. Me ei vaadanud ainult tööriistade nimesid, vaid mõtlesime, milliseid ülesandeid uus analüütik päriselt tegema hakkab: müügiandmete analüüs, kliendisegmentide leidmine, dashboardide koostamine ja andmete puhastamine.

Seejärel jagasime töö nelja liikme vahel. Üks liige vaatas, kuidas tehnilised oskused peaksid CV-s ja kandideerimisel välja paistma. Teine liige koostas praktilise testi SQL-i ja Pythoniga. Kolmas liige keskendus sellele, kuidas kandidaat käitub probleemi lahendades. Neljas liige hindas, kas kandidaat sobiks igapäevasesse tiimitöösse ja oskaks oma tulemusi teistele selgitada.

Pärast individuaalset tööd võrdlesime oma tähelepanekuid ja panime kokku ühise hindamisjuhendi. Eesmärk oli, et Toomas Kask saaks seda kasutada nii tehnilise intervjuu ettevalmistamisel kui ka kandidaatide võrdlemisel.

## Mida kandidaadilt oodatakse

Kandidaadilt ei eeldata senior-taseme oskuseid, aga oodatakse tugevat põhja. Junior andmeanalüütik peaks oskama kirjutada lihtsamaid ja keskmise raskusega SQL-päringuid, ühendada tabeleid JOIN-idega, kasutada GROUP BY loogikat ning kontrollida, kas saadud tulemused on loogilised.

Pythonis oodatakse vähemalt pandas teegi baastaset: andmete lugemine, filtreerimine, grupeerimine, puuduvate väärtuste kontroll ja lihtsad kokkuvõtted. Samuti on oluline, et kandidaat mõistaks andmete visualiseerimise eesmärki. Dashboard ei ole lihtsalt ilus graafik, vaid tööriist otsuste tegemiseks.

Lisaks tehnilistele oskustele oodatakse kandidaadilt, et ta oskab oma mõttekäiku selgitada. Kui lahendus ei tule kohe välja, peaks kandidaat oskama öelda, mida ta prooviks järgmisena ja millist infot ta juurde vajaks.

## Mida tööandja vaatab

Tööandja vaatab, kas kandidaadi tehnilised oskused on praktilised. Näiteks ei piisa sellest, et kandidaat ütleb "oskan SQL-i". Ta peab suutma näidata, kuidas ta kasutab SQL-i äriküsimusele vastamiseks.

Vaadatakse ka seda, kas kandidaat kontrollib oma tulemusi. Kui müüginumbrid tunduvad ebaloogilised, peaks analüütik seda märkama ja uurima, kas probleem on andmetes, päringus või äriloogikas.

Oluline on ka dokumenteerimine. Kui kandidaat kirjutab keerulisema päringu või Python-skripti, peaks tema töö olema loetav ka teisele inimesele. UrbanStyle'i tiimis ei tööta analüütik üksi, seega peab tema töö olema arusaadav ja edasi kasutatav.

## Hindamise viis

Hindamiseks sobib lühike praktiline ülesanne, mis põhineb UrbanStyle'i tüüpi andmetel. Kandidaadile antakse müügi-, kliendi- ja tooteandmed ning palutakse leida mõned äriliselt olulised vastused.

Hindamisel tuleks vaadata nelja asja:

- kas tehniline lahendus töötab
- kas kandidaat selgitab oma mõttekäiku
- kas tulemus on äriliselt arusaadav
- kas töö on piisavalt loetav ja kontrollitud

Kõige tugevam kandidaat ei pruugi olla see, kes kirjutab kõige keerulisema koodi, vaid see, kes lahendab probleemi loogiliselt ja oskab tulemuse ettevõtte jaoks tähenduslikuks teha.

## Alaülesanne A: tehniliste nõuete kirjeldamine

Palkamisjuhi vaates tuleb kirjeldada, millised tehnilised oskused peaksid junior andmeanalüütikul kindlasti olemas olema. Minu hinnangul peaksid põhioskused olema SQL, Excel, Python, andmete visualiseerimine ja GitHubi kasutamine. SQL-i puhul ei piisa ainult SELECT-päringust, vaid kandidaat peaks oskama kasutada WHERE, GROUP BY, JOIN, HAVING ja lihtsamaid CTE-sid.

Tööandja jaoks on oluline, et oskused oleksid seotud ärilise tulemusega. Näiteks parem on kirjutada "analüüsisin 10 000+ müügikirjet ja leidsin 245 VIP-klienti" kui lihtsalt "oskan SQL-i".

## Alaülesanne B: tehnilise testi koostamine

Tehnilise intervjueerija ülesanne on pakkuda välja testülesanded. UrbanStyle'i kontekstis võiks kandidaat saada väikese müügiandmestiku ning kolm ülesannet:

1. Leia iga tootekategooria kogumüük ja tellimuste arv.
2. Ühenda kliendi-, müügi- ja tooteandmed JOIN-idega.
3. Leia kliendid, kelle ostusagedus ja koguväärtus viitavad VIP-segmendile.

Pythonis võiks ülesanne olla lihtne andmepuhastus pandas teegiga: puuduvate väärtuste kontroll, duplikaatide eemaldamine ja müügi koondamine kliendi kaupa. Kandidaadilt ei peaks ootama perfektset lahendust, vaid loogilist mõtlemist ja oskust selgitada, mida ta teeb.

## Alaülesanne C: hindamiskriteeriumid

Personalijuhi vaates tuleb hinnata ka seda, kuidas kandidaat tehnilist probleemi lahendab. Kui ta jääb kinni, siis oluline ei ole kohe valmis vastus, vaid see, kas ta oskab küsida täpsustavaid küsimusi ja selgitada oma mõttekäiku.

Rohelised lipud:

- kandidaat selgitab oma lahendust samm-sammult
- kandidaat kontrollib tulemusi, mitte ei usalda pimesi esimest päringut
- kandidaat seob tehnilise tulemuse äriküsimusega
- kandidaat dokumenteerib või kommenteerib keerulisemat loogikat

Punased lipud:

- kandidaat ei oska selgitada, mida tema kood teeb
- tulemused on arvuliselt ebaloogilised, aga kandidaat ei märka seda
- kandidaat räägib ainult tööriistadest, mitte probleemilahendusest
- kandidaat ei tunne põhilisi SQL JOIN-e või agregatsioone

## Peatüki lõppväljund

Toomas Kasele soovitame kasutada lühikest praktilist testi, kus kandidaat peab töötama UrbanStyle'i tüüpi müügiandmetega. Hindamisel tuleks arvestada nii tehnilist täpsust kui ka seda, kas kandidaat oskab tulemusi äriliselt tõlgendada.

## Rollide vaade ja alaülesannete sooritamise tulemus 4-liikmelises rühmas

**Liige 1 ehk Roll A: palkamisjuhi vaade**

Tulemuseks koostas liige 1 nimekirja tehnilistest põhioskustest, mida junior andmeanalüütiku CV-s ja kandideerimismaterjalides otsida. Tema järeldus oli, et SQL, Python, Excel, visualiseerimine ja GitHub peaksid olema seotud konkreetsete projektidega, mitte ainult oskuste loeteluna välja toodud.

**Liige 2 ehk Roll B: tehnilise intervjueerija vaade**

Tulemuseks pakkus liige 2 välja praktilise tehnilise testi UrbanStyle'i müügiandmete põhjal. Test sisaldab SQL-i ülesandeid kategooriate müügi, JOIN-ide ja VIP-kliendi leidmise kohta ning lihtsat Python/pandas andmepuhastuse ülesannet.

**Liige 3 ehk Roll C: personalijuhi vaade**

Tulemuseks kirjeldas liige 3, kuidas hinnata kandidaadi käitumist tehnilise ülesande ajal. Ta tõi välja, et oluline on kandidaadi oskus selgitada oma mõttekäiku, küsida täpsustavaid küsimusi ja reageerida rahulikult, kui ta kohe vastust ei tea.

**Liige 4 ehk Roll D: tiimijuhi vaade**

Tulemuseks lisas liige 4 hindamisse tiimitöö ja igapäevase töö praktilise vaate. Tema rõhutas, et tulevane analüütik peab oskama oma päringuid dokumenteerida, tulemusi kontrollida ja selgitada neid teistele osakondadele arusaadavalt.

**Rühma ühine tulemus**

Rühm jõudis järeldusele, et tehniliste oskuste hindamine peab olema praktiline ja seotud UrbanStyle'i ärikontekstiga. Ainult teooriaküsimustest ei piisa, sest tööandja peab nägema, kuidas kandidaat kasutab andmeid päris probleemi lahendamiseks.
