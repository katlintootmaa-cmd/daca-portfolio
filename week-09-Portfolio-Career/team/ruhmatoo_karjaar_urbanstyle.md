# Rühmatöö: UrbanStyle andmeanalüütikute värbamisjuhend

## Sissejuhatus

UrbanStyle kasvab kiiresti ja ettevõttel on vaja palgata uusi andmeanalüütikuid Tallinna, Tartusse, Pärnusse ning osaliselt ka kaugtööle. Liis Koppel, UrbanStyle'i operatsioonijuht, palub meie abi, sest me oleme 8 nädalat töötanud UrbanStyle'i andmetega ja mõistame juba päris hästi, milliseid oskusi andmeanalüütik igapäevatöös vajab.

Meie rühmatöö eesmärk on koostada UrbanStyle'i juhtidele praktiline värbamisjuhend. Juhend aitab hinnata kandidaadi tehnilisi oskusi, portfooliot, CV-d, LinkedIni profiili, intervjuuvalmidust ja sisseelamise plaani. Kuna meie meeskonnas on 4 liiget, jagasime töö rollide kaupa ning koostasime peatükid ühiselt.

Minu arvates on tööandja vaatepunkt hea lähenemine, sest nii ei pea keegi oma isiklikku CV-d kogu grupile näitama. Selle asemel mõtleme koos läbi, mida tööandja tegelikult otsib, ja igaüks saab hiljem oma materjale selle põhjal ise parandada.

## Rühmatöö üldine töökorraldus 4-liikmelises meeskonnas

Töö toimub JAGA-TEE-KOGU-ESITLE põhimõttel. Kõigepealt jagasime nelja liikme vahel rollid, seejärel tegi iga liige oma alaülesande. Pärast seda koondasime tulemused ühiseks värbamisjuhendiks ning lõpus valisime välja olulisemad järeldused, mida esitleda.

Kuna meie meeskonnas on 4 liiget, jagasime töö nelja põhirolli vahel:

- Roll A: palkamisjuhi vaade ehk CV ja LinkedIni hindamine
- Roll B: tehnilise intervjueerija vaade ehk koodi, SQL-i, Pythoni ja tööriistade hindamine
- Roll C: personalijuhi vaade ehk pehmed oskused ja meeskonda sobivus
- Roll D: tiimijuhi vaade ehk koostöövõime, iseseisvus ja kommunikatsioon

Juhatuse liikme vaate ehk ärimõju ning kandidaadi vaate ehk värbamisprotsessi selguse arutasime läbi ühiselt, sest need puudutavad kõiki peatükke. Nii sai iga liige keskenduda oma põhivaatele, aga lõpptulemus jäi terviklik.

### Meeskonnaliikmete alaülesanded

**Liige 1 ehk Roll A: palkamisjuhi vaade**

Tema vastutab selle eest, et juhendis oleks selgelt kirjeldatud, kuidas hinnata kandidaadi CV-d, LinkedIni profiili ja üldist professionaalset esitlust. Ta vaatab, kas kandidaadi oskused on esitatud konkreetselt, kas tulemused on mõõdetavad ja kas portfoolio toetab CV-s kirjutatut.

**Liige 2 ehk Roll B: tehnilise intervjueerija vaade**

Tema vastutab tehniliste oskuste hindamise eest. Ta koostab ettepanekud SQL-i, Pythoni, GitHubi ja dashboardide hindamiseks ning pakub välja praktilise testi, millega saab kontrollida kandidaadi päris oskusi.

**Liige 3 ehk Roll C: personalijuhi vaade**

Tema keskendub pehmetele oskustele, meeskonda sobivusele ja suhtlemisele. Ta hindab, kuidas kandidaadi portfoolio ja intervjuuvastused näitavad õppimisvõimet, koostööd, vastutustunnet ja oskust küsida abi.

**Liige 4 ehk Roll D: tiimijuhi vaade**

Tema vaatab kandidaati tulevase tiimiliikmena. Ta keskendub sellele, kas kandidaat suudab töötada iseseisvalt, anda oma töö kohta selgeid vahekokkuvõtteid, dokumenteerida tulemusi ja suhelda teiste osakondadega.

## Peatükk 1: tehniliste oskuste hindamine

### Eesmärk

Esimese grupi ülesanne on koostada juhend Toomas Kasele, kes on UrbanStyle'i IT-direktor. Tema tahab teada, kuidas hinnata, kas kandidaat oskab päriselt andmetega töötada või on ta ainult CV-sse tööriistade nimed kirjutanud.

### Alaülesanne A: tehniliste nõuete kirjeldamine

Palkamisjuhi vaates tuleb kirjeldada, millised tehnilised oskused peaksid junior andmeanalüütikul kindlasti olemas olema. Minu hinnangul peaksid põhioskused olema SQL, Excel, Python, andmete visualiseerimine ja GitHubi kasutamine. SQL-i puhul ei piisa ainult SELECT-päringust, vaid kandidaat peaks oskama kasutada WHERE, GROUP BY, JOIN, HAVING ja lihtsamaid CTE-sid.

Tööandja jaoks on oluline, et oskused oleksid seotud ärilise tulemusega. Näiteks parem on kirjutada "analüüsisin 10 000+ müügikirjet ja leidsin 245 VIP-klienti" kui lihtsalt "oskan SQL-i".

### Alaülesanne B: tehnilise testi koostamine

Tehnilise intervjueerija ülesanne on pakkuda välja testülesanded. UrbanStyle'i kontekstis võiks kandidaat saada väikese müügiandmestiku ning kolm ülesannet:

1. Leia iga tootekategooria kogumüük ja tellimuste arv.
2. Ühenda kliendi-, müügi- ja tooteandmed JOIN-idega.
3. Leia kliendid, kelle ostusagedus ja koguväärtus viitavad VIP-segmendile.

Pythonis võiks ülesanne olla lihtne andmepuhastus pandas teegiga: puuduvate väärtuste kontroll, duplikaatide eemaldamine ja müügi koondamine kliendi kaupa. Kandidaadilt ei peaks ootama perfektset lahendust, vaid loogilist mõtlemist ja oskust selgitada, mida ta teeb.

### Alaülesanne C: hindamiskriteeriumid

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

### Peatüki 1 lõppväljund

Toomas Kasele soovitame kasutada lühikest praktilist testi, kus kandidaat peab töötama UrbanStyle'i tüüpi müügiandmetega. Hindamisel tuleks arvestada nii tehnilist täpsust kui ka seda, kas kandidaat oskab tulemusi äriliselt tõlgendada.

## Peatükk 2: portfoolio hindamine

### Eesmärk

Teise grupi ülesanne on koostada juhend Kristi Tammele, UrbanStyle'i CEO-le. Kristi ei pruugi ise koodi detailselt hinnata, aga ta tahab aru saada, kas kandidaadi portfoolio näitab ärilist mõtlemist ja tööks valmisolekut.

### Alaülesanne A: GitHubi üldmulje

Palkamisjuhi vaates peaks portfoolio olema korrastatud ja kiiresti arusaadav. Kui GitHubis on ainult failid ilma selgituseta, siis tööandjal on raske hinnata, mida kandidaat tegelikult tegi. Iga projekti juures peaks olema README, kus on kirjas:

- mis oli äriprobleem
- milliseid andmeid kasutati
- milliseid tööriistu kasutati
- milline oli tulemus
- mida kandidaat õppis või parandaks järgmisel korral

### Alaülesanne B: tehniline kvaliteet

Tehnilise intervjueerija vaates tuleks vaadata, kas kood on loetav, failid on loogiliselt nimetatud ja päringud ei ole lihtsalt juhuslikud katsetused. Hea portfoolio ei pea olema täiuslik, aga see peab näitama mõtlemise arengut.

Näiteks UrbanStyle'i portfoolios võiks tugevaks projektiks olla RFM-kliendisegmenteerimine, kus kandidaat näitab, kuidas ta leidis väärtuslikud kliendid ja muutis tulemuse dashboardiks või ärisoovituseks.

### Alaülesanne C: äriline väärtus

CEO vaates on kõige tähtsam küsimus: "Mida ettevõte selle teadmisega teha saab?" Kui kandidaat näitab ainult graafikut, aga ei ütle, mida see tähendab, on töö poolik. Kui ta aga selgitab, et VIP-kliendid moodustavad väikse osa kliendibaasist, kuid annavad suure osa käibest, siis on see juba äriline insight.

### Peatüki 2 lõppväljund

Kristi Tammele soovitame portfoolio hindamiseks kontrollnimekirja: selge README, vähemalt 2-3 tugevat projekti, mõõdetavad tulemused, nähtav ärimõju ja korrektne tehniline teostus. Kandidaat peaks suutma oma portfooliot 3-5 minutiga arusaadavalt tutvustada.

## Peatükk 3: CV ja LinkedIni hindamine

### Eesmärk

Kolmanda grupi ülesanne on aidata Anna Metsal hinnata andmeanalüütiku CV-d ja LinkedIni profiili. Anna turundusjuhina pöörab tähelepanu sellele, kuidas kandidaat ennast esitleb ja kas tema väärtus on kiiresti mõistetav.

### Alaülesanne A: CV hindamine

Hea junior andmeanalüütiku CV peaks olema lühike, konkreetne ja ATS-sõbralik. Seal peaksid olema kontaktandmed, lühikokkuvõte, tehnilised oskused, projektid, töökogemus ja haridus. Karjäärivahetaja puhul on oluline siduda varasem kogemus uute andmeoskustega.

Hea CV lause:

"Analüüsisin 10 000+ UrbanStyle'i müügikirjet SQL-i ja Pythoniga, tuvastades 245 VIP-klienti väärtusega 127 000 eurot."

Nõrk CV lause:

"Töötasin andmetega ja koostasin raporteid."

Erinevus on selles, et esimene lause näitab tegevust, tööriistu ja tulemust. Teine lause on liiga üldine.

### Alaülesanne B: LinkedIni hindamine

LinkedIni pealkiri peaks sisaldama rolli, oskusi ja väärtuspakkumist. Näiteks:

"Junior Data Analyst | SQL, Python, Power BI | Turning Data into Business Insights"

About-sektsioon võiks rääkida kandidaadi loo: kust ta tuleb, mida ta õppis, milliseid projekte tegi ja millist väärtust ta tööandjale pakub. Featured-sektsioonis võiksid olla GitHubi portfoolio, dashboard või parim projekt.

### Alaülesanne C: punased ja rohelised lipud

Rohelised lipud:

- CV-s on mõõdetavad tulemused
- oskused kattuvad tööpakkumisega
- GitHub ja LinkedIn on lisatud
- LinkedInis on selge pealkiri ja projektid nähtaval
- varasem töökogemus on seotud andmeanalüütika rolliga

Punased lipud:

- CV on liiga üldine ja ilma numbriteta
- oskuste nimekiri on pikk, aga projektid ei tõesta neid
- LinkedIn on tühi või vananenud
- GitHubi link puudub
- kandidaat kasutab ainult klišeesid nagu "olen motiveeritud ja töökas"

### Peatüki 3 lõppväljund

Anna Metsale soovitame hinnata CV-d ja LinkedIni kui kandidaadi professionaalset turundusmaterjali. Hea kandidaat ei pea olema kõige kogenum, aga tema profiilist peab kiiresti aru saama, mida ta oskab ja millist väärtust ta UrbanStyle'ile looks.

## Peatükk 4: 30-60-90 päeva sisseelamisplaan

### Eesmärk

Neljanda grupi ülesanne on koostada Marko Saarele uue analüütiku sisseelamisplaan. Plaan peab sobima nii kontoris töötavale kui ka remote-kolleegile Soomes või Saksamaal.

### Esimesed 30 päeva

Esimese kuu eesmärk on õppida süsteeme, inimesi ja äriloogikat. Uus analüütik peaks tutvuma UrbanStyle'i andmebaasidega, peamiste KPI-dega ja osakondade vajadustega. Ta võiks teha esimesed lihtsad SQL-päringud ning korrata olemasolevaid raporteid, et mõista, kuidas ettevõttes andmeid kasutatakse.

Oluline on määrata mentor, kes aitab uuel töötajal küsimustele vastuseid leida. Remote-töötajale peaks olema lisaks selge suhtluskanal, näiteks regulaarne check-in Google Meetis või Teamsis.

### Päevad 30-60

Teisel kuul võiks uus analüütik hakata tegema iseseisvamaid ülesandeid. Näiteks analüüsida müügitrende, täiendada dashboardi või teha kliendisegmenteerimise lihtsam versioon. Selles etapis peaks ta juba oskama küsida äriküsimusi, mitte ainult täita tehnilist ülesannet.

### Päevad 60-90

Kolmandal kuul võiks uus analüütik võtta enda peale ühe väikese projekti algusest lõpuni. Näiteks kampaania tulemuste analüüs, varude optimeerimise raport või RFM-segmenteerimise uuendamine. Lõpus peaks ta esitama tulemused tiimile ja pakkuma vähemalt 2-3 praktilist soovitust.

### Peatüki 4 lõppväljund

Marko Saarele soovitame 30-60-90 päeva plaani, mis liigub Shu-Ha-Ri põhimõttel: alguses õpitakse ja jäljendatakse, siis kohandatakse ning lõpuks tehakse iseseisev panus. Remote onboarding peab olema eriti selge, sest kaugtöötaja vajab rohkem struktureeritud suhtlust.

## Peatükk 5: tööpakkumise kirjutamine

### Eesmärk

Viienda grupi ülesanne on koostada Liis Koppelile andmeanalüütiku tööpakkumise põhi. Töökuulutus peab olema aus, konkreetne ja oskuspõhine. See ei tohiks kasutada ebamääraseid väljendeid nagu "data ninja" või "rockstar analyst".

### Töökuulutuse sisu

Töökuulutus peaks algama selge kirjeldusega, miks UrbanStyle analüütikut vajab. Näiteks:

"UrbanStyle otsib junior andmeanalüütikut, kes aitaks muuta müügi-, kliendi- ja tooteandmed otsusteks. Sinu töö aitab juhtidel paremini mõista müügitrende, kliendisegmente ja varude liikumist."

Nõuded võiksid olla realistlikud:

- SQL-i põhioskus, sh JOIN ja GROUP BY
- Python või valmisolek Pythonit töös kasutada
- andmete visualiseerimise oskus Power BI, Tableau, Plotly või sarnase tööriistaga
- oskus selgitada tulemusi mitte-tehnilistele inimestele
- GitHubi või portfoolio olemasolu on eelis

### Kandidaadile pakutav väärtus

Hea tööpakkumine ei nõua ainult kandidaadilt, vaid näitab ka, mida ettevõte pakub. UrbanStyle võiks pakkuda mentorlust, päris äriprobleeme, paindlikku töökorraldust ja võimalust areneda BI või business analyst suunas.

### Peatüki 5 lõppväljund

Liis Koppelile soovitame tööpakkumist, mis on aus ja konkreetne. See peaks kutsuma kandideerima ka karjäärivahetajaid, kellel on tugev portfoolio ja äriline mõtlemine, isegi kui neil ei ole veel mitmeaastast ametlikku andmeanalüütiku kogemust.

## Peatükk 6: intervjuu stsenaarium

### Eesmärk

Kuuenda grupi ülesanne on koostada intervjuu stsenaarium kogu UrbanStyle'i juhatusele. Intervjuu peab hindama nii tehnilisi oskusi, pehmeid oskusi kui ka ärilist mõtlemist.

### Intervjuu struktuur

Soovitame 60-minutilist intervjuud:

- 5 minutit: sissejuhatus ja kandidaadi tausta kuulamine
- 15 minutit: portfoolio walk-through
- 15 minutit: tehniline SQL või Python ülesanne
- 15 minutit: STAR-meetodil käitumuslikud küsimused
- 5 minutit: kandidaadi küsimused
- 5 minutit: järgmiste sammude selgitamine

### Näidisküsimused

Tehniline küsimus:

"Kuidas leiaksid SQL-iga iga kategooria kolm enim müüdud toodet?"

Äriline küsimus:

"Kui dashboard näitab, et müük kasvab, aga kasum väheneb, mida sa edasi uuriksid?"

STAR-küsimus:

"Räägi olukorrast, kus pidid meeskonnas ajasurve all andmeprobleemi lahendama."

Portfoolio küsimus:

"Milline sinu projekt näitab kõige paremini, et oskad andmeid äriliseks otsuseks muuta?"

### Hindamiskriteeriumid

Kandidaat võiks intervjuu läbida, kui ta:

- oskab selgitada oma portfooliot arusaadavalt
- lahendab tehnilise ülesande loogiliselt või vähemalt mõtleb struktureeritult
- seob andmeanalüüsi äriprobleemiga
- oskab tuua konkreetseid näiteid oma koostööst ja probleemilahendusest
- küsib intervjuu lõpus sisukaid küsimusi ettevõtte ja andmetiimi kohta

### Peatüki 6 lõppväljund

Juhatusele soovitame intervjuud, mis ei keskendu ainult tehnilisele testile. Hea andmeanalüütik peab oskama kirjutada päringuid, aga sama oluline on oskus tulemusi selgitada ja pakkuda otsustamiseks kasulikke soovitusi.

## Ühine kokkuvõte

Meie 4-liikmelise meeskonna töö tulemusena valmis UrbanStyle'i andmeanalüütiku värbamisjuhend. Meie peamine järeldus on, et hea junior andmeanalüütik ei pea olema ekspert kõigis tööriistades, aga ta peab suutma näidata kolme asja: tehnilist baasi, ärilist mõtlemist ja õppimisvõimet.

UrbanStyle'i jaoks on tugev kandidaat inimene, kes oskab SQL-i ja Pythonit vähemalt praktilisel tasemel, suudab portfoolios näidata reaalseid projekte, kirjutab CV-s tulemused numbritega lahti ning oskab intervjuul oma tööd selgitada nii tehnilisele kui ka mitte-tehnilisele kuulajale.

See rühmatöö aitas mul paremini aru saada, mida tööandja tegelikult otsib. Kõige olulisem ei ole kirjutada CV-sse võimalikult palju oskusi, vaid tõestada neid konkreetsete projektide ja tulemustega. UrbanStyle'i näitel saab hästi näidata, kuidas andmeanalüütika loob ettevõttele väärtust: paremad kliendisegmendid, selgemad dashboardid, kiirem raportite koostamine ja täpsemad juhtimisotsused.

## Minu isiklik refleksioon

Selle töö põhjal saan ka enda karjäärimaterjale paremini hinnata. Kui tööandja otsib tehnilisi oskusi, portfooliot, selget LinkedIni profiili ja konkreetseid tulemusi, siis peaksin ka oma CV-s ja GitHubis keskenduma just nendele asjadele. Minu jaoks oli kõige kasulikum mõte see, et varasem kogemus ei ole puudus, vaid võib olla eelis, kui oskan selle siduda uute andmeoskustega.

Edasi peaksin üle vaatama, kas minu portfoolio projektidel on piisavalt selged README-d, kas CV-s on tulemused numbritega esitatud ja kas LinkedIni profiil näitab kohe, et otsin andmeanalüütiku või BI analyst rolli. Samuti peaksin ette valmistama 2-3 STAR-vastust UrbanStyle'i projektide põhjal, et intervjuul oleks lihtsam oma kogemust selgitada.
