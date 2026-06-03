# Nädal 10 tiimitöö: Portfoolio kaitsmine

English version: [README_EN.md](README_EN.md)

## Ülesande eesmärk

Nädala 10 tiimitöö eesmärk oli valmistada ette 7-minutiline UrbanStyle'i juhatuse koosoleku formaadis portfoolio kaitsmine. Esitlus pidi vastama küsimusele:

> Mida UrbanStyle tegelikult meie andmetööst õppis ja milline otsus võiks selle põhjal muutuda?

Fookus oli mõjul, mitte tehtud failide loetlemisel. Seetõttu koondasime 10 nädala töö üheks äriliseks looks: andmeprobleemid, peamised leiud, tugevamad visualiseeringud, juhatusele mõeldud soovitused ja AI kasutamise refleksioon.

## Meeskonna missioon

Meie meeskonna missioon oli aidata UrbanStyle'il liikuda tunnetuspõhiselt otsustamiselt andmepõhisema juhtimise poole. Selleks kasutasime SQL-i, Power BI-d, Python/Pandast, API pipeline'i ja GitHubi dokumentatsiooni, et muuta müügi-, kliendi- ja raportiandmed otsusteks kasutatavaks.

## Rollijaotus

| Roll | Tiimiliige | Vastutus |
|------|------------|----------|
| Portfoolio kvaliteedikontroll | Kätlin | README-de struktuur, projektide äriline selgitus, tõendusmaterjalid ja kaitsmise loogika |
| Deploy ja linkide kontroll | Ragnar | Avalik ligipääs, katkised lingid, failide avanemine ja tehniline kasutatavus |
| Tehniline ülevaatus | Karmo | SQL/Python failid, notebookid, pipeline'id ja reprodutseeritavus |
| Esitlus ja äriline sõnum | Mari | Väärtuspakkumine, juhatuse soovitused, üleminekud ja data storytelling |

Minu roll oli portfoolio kvaliteedikontroll. Kontrollisin, et töö oleks arusaadav ka inimesele, kes ei tea kursuse tausta: igal olulisel projektil peab olema probleem, lähenemine, tulemus, õppetund ja selgitus AI kasutamise kohta.

## 7-minutilise esitluse plaan

| Osa | Aeg | Rääkija | Sisu |
|-----|-----|---------|------|
| Sissejuhatus | 1:00 | Mari | Meeskond, missioon ja UrbanStyle'i kontekst |
| Andmete ülevaade | 2:00 | Karmo | 3-5 peamist numbrilist leidu ja suurim üllatus |
| Visualiseeringud | 2:00 | Kätlin | Power BI dashboardid, RFM väljundid ja API/Plotly näited |
| Soovitused juhatusele | 1:00 | Mari | 3 konkreetset andmepõhist soovitust |
| AI kasutamine | 1:00 | Ragnar | Kuidas AI aitas ning kus pidime ise otsustama |

## Peamised leiud, mida esitluses kasutada

| Leid | Tõend | Miks see juhatusele oluline on |
|------|------|--------------------------------|
| 2024. aasta käive kasvas võrreldes 2023. aastaga 19.08%. | [Power BI investorivaade](../../week-05-Visualization-Design/individual/README.md) | UrbanStyle on kasvulooline ettevõte, kuid juhtkond peab jälgima, millised kanalid ja kategooriad kasvu veavad. |
| RFM analüüsi puhastatud andmestikus jäi alles 8,950 müügirida ja 2,540 unikaalset klienti. | [RFM andmepuhastus Pythonis](../../week-07-Python-Pandas/individual/README.md) | Kliendisegmenteerimine põhineb piisavalt suurel ja kontrollitud andmestikul. |
| VIP Champions segment annab suure osa käibest, kuigi see ei ole kõige suurem kliendigrupp. | [RFM tiimitöö väljundid](../../week-07-Python-Pandas/team/README.md) | Turunduse ja lojaalsusprogrammi fookus peaks olema väärtuslikematel klientidel, mitte ainult suurimal kliendigrupil. |
| Tallinn on UrbanStyle'i peamine füüsiline müügikoht ja sobib teiste kaupluste võrdluspunktiks. | [Tallinna kaupluse dashboard](../../week-06-Visualization-Storytelling/individual/README.md) | Juhtkond saab kasutada Tallinna toimivaid mustreid teiste asukohtade arendamisel. |
| API pipeline muutis korduvad raportiväljundid taaskasutatavaks. | [API pipeline](../../week-08-API-Pipeline/individual/README.md) | Automatiseerimine vähendab käsitööd ja aitab raportite kvaliteeti ühtlasemana hoida. |

## Näidatavad visuaalid

1. [UrbanStyle investori dashboard](../../week-05-Visualization-Design/individual/week%205%20D.png) - näitab kasvu, KPI-sid ja investori jaoks olulist üldpilti.
2. [Tallinna kaupluse dashboard](../../week-06-Visualization-Storytelling/individual/week%206_A_K%C3%A4tlin.png) - näitab asukohapõhist andmelugu ja juhtkonna vaadet.
3. [RFM segmentide scatter plot](../../week-07-Python-Pandas/team/rfm_segmentide_scatter.png) - näitab kliendisegmentide erinevust ja VIP klientide väärtust.
4. [API pipeline'i HTML-väljund](../../week-08-API-Pipeline/individual/combined_visuals.html) - näitab, et analüüsi väljundit saab automatiseerida ja jagada.

## 3 soovitust UrbanStyle'i juhatusele

1. Kasutada Power BI dashboarde iganädalases juhtimisrütmis, sest 19.08% aastane käibekasv vajab regulaarset kanalite, kategooriate ja kaupluste jälgimist.
2. Suunata lojaalsus- ja turundustegevused väärtuslikematele RFM segmentidele, sest VIP Champions segment annab suure osa käibest, kuigi segment ei ole klientide arvult kõige suurem.
3. Automatiseerida korduvad raportid Python/API pipeline'i abil, et vähendada käsitsi tehtavat tööd, hoida väljundid järjepidevana ja teha andmete kontroll korduvkasutatavaks.

## Lühike esitluse tekst

**Sissejuhatus:**
Tere, meie oleme UrbanStyle'i andmemeeskond. Meie missioon oli muuta 10 nädala jooksul müügi-, kliendi- ja raportiandmed juhtkonnale kasutatavaks. Me ei keskendunud ainult päringutele ja dashboardidele, vaid sellele, mida UrbanStyle saab nende põhjal otsustada.

**Andmete ülevaade:**
Meie töö kõige tugevam kasvunumber oli see, et 2024. aasta käive kasvas võrreldes 2023. aastaga 19.08%. RFM analüüsi jaoks puhastasime andmestiku nii, et alles jäi 8,950 müügirida ja 2,540 unikaalset klienti. Suurim äriline üllatus oli, et VIP Champions segment annab suure osa käibest, kuigi see ei ole kõige suurem kliendigrupp.

**Visualiseeringud:**
Investorivaade näitab kasvu ja peamisi KPI-sid ühelt ekraanilt. Tallinna kaupluse dashboard näitab, kuidas üks tugev füüsiline müügikoht saab olla teiste asukohtade võrdluspunkt. RFM visualiseeringud aitavad näha, millised kliendid väärivad eraldi tähelepanu. API pipeline'i väljund näitab, et samu samme saab korrata ilma iga kord käsitsi raportit ehitamata.

**Soovitused:**
Meie soovitus juhatusele on kasutada dashboarde regulaarselt, mitte ainult projekti lõpus. Teiseks tuleks lojaalsus- ja turundustegevused siduda RFM segmentidega. Kolmandaks tuleks korduvad raportid automatiseerida, sest see säästab aega ja vähendab käsitsi vigade riski.

**AI kasutamine:**
AI aitas meid SQL-i ja Python koodi debug'imisel, README-de selgemaks kirjutamisel, esitluse struktuuri kontrollimisel ja kaitseküsimuste läbimõtlemisel. Samas kontrollisime numbrid, ärijäreldused ja lõplikud soovitused ise, sest AI ei asenda UrbanStyle'i konteksti mõistmist ega analüütiku vastutust.

## Ajaproovi kontrolltabel

| Osa | Sihtaeg | Kontroll |
|-----|---------|----------|
| Sissejuhatus | 1:00 | Mahub siis, kui missioon on üks lause ja liikmete tutvustus lühike |
| Andmete ülevaade | 2:00 | Iga leid = üks lause + üks number |
| Visualiseeringud | 2:00 | Näidata 2-3 visuaali, mitte kõiki faile |
| Soovitused | 1:00 | Täpselt 3 soovitust |
| AI kasutamine | 1:00 | 2-3 konkreetset näidet + üks õppetund |
| Kokku | 7:00 | 6:00 juures kollane signaal, 7:00 juures lõpetada lause |

## Kvaliteedikontroll enne kaitsmist

- Esitlus järgib 5-osalist struktuuri.
- Esitlus mahub 7 minuti sisse.
- Vähemalt 3 numbrilist leidu on valmis.
- Vähemalt 1 tugev visuaal või dashboard avaneb kiiresti.
- 3 juhatusele mõeldud soovitust on konkreetsed ja andmepõhised.
- AI kasutamise refleksioon on aus ja konkreetne.
- Iga tiimiliige teab oma osa ja üleminekud on kokku lepitud.
- GitHubi lingid, README-d, Power BI ekraanipildid ja HTML-väljundid avanevad.

## Õpitu

Tiimitöö suurim õppetund oli, et portfoolio kaitsmine peab rääkima mõjust, mitte protsessist. Juhatus ei vaja pikka nimekirja kõigist päringutest ja failidest. Juhatus vajab vastust küsimusele: mida andmed näitasid ja mida UrbanStyle peaks selle põhjal tegema?

Samuti õppisime, et hea portfoolio on koostöö tõend. Tehniline töö, visualiseeringud, ärisoovitused ja selge dokumentatsioon peavad koos moodustama loo, mida saab kiiresti mõista ja kontrollida.
