# Tiimi töö kokkuvõte - Nädal 1: SQL Basics

## Meeskonna üldine tööprotsess
Meeskond järgis DACA raamistikku JAGA-TEE-KOGU-ESITLE, jagades töö andmedomeenide järgi. Iga liige võttis vastutuse ühe andmevaldkonna eest: müügiandmed, kliendiandmed, tooteandmed ja müügikanalid.

## Peamised tegevused
- **JAGA**: Rollide jaotamine vastavalt meeskonna suurusele (4-liikmeline meeskond: müügitehingud, kliendiandmed, tooteandmed, müügikanalid)
- **TEE**: Iseseisev töö oma domeeniga, kasutades SQL päringuid (SELECT, WHERE, ORDER BY, DISTINCT, COUNT)
- **KOGU**: Tulemuste kokkupanek ja 3 sünteesiküsimuse arutelu
- **ESITLE**: Meeskondade esitlused ja tagasiside

## Võtmeleiud andmete analüüsist
- **Müügiandmed**: 15,234 tehingut, suurim tehing 2,170.4 EUR, väikseim -1,405.32 EUR, 1,487 puuduvat kliendi ID-d, 5,204 puuduvat kaupluse asukohta, palju negatiivseid tehinguid
- **Kliendiandmed**: 3,150 klienti, e-maile: 3,150 kokku, 2,640 unikaalsed, 510 duplikaati, 380 puudu, vanim klient 2020-01-02, uusim 2025-02-27, linnad vajavad puhastamist
- **Tooteandmed**: 362 toodet, kategooriad: jalanõud, lasteriided, aksessuaarid, naisteriided, meesteriided, hinnavahemik 13.53-434.08 EUR, puuduvaid andmeid ei olnud
- **Müügikanalid**: Online 5,204 tehingut, pood 10,030 tehingut, asukohad: Tallinn, Tartu, Pärnu, enim müüki Tallinnas

## Peamised probleemid tuvastatud
1. Palju negatiivseid tehinguid müügiandmetes
2. Puuduvad kliendi ID-d (1,487 tehingut) ja kaupluse asukohad (5,204 tehingut)
3. E-mailide duplikaadid (510) ja puuduvad e-mailid (380 klient)
4. Linnade andmete ebajärjekindlus ja vajadus puhastamise järele

## Soovitused Toomasele
- Andmete puhastamine ja kvaliteedikontrolli lisamine
- Eraldi analüüs online ja offline kanalite jaoks
- Kliendiandmete (eriti e-mailide) paremaks kogumiseks

## Meeskonna õppetunnid
- SQL põhioperatsioonide rakendamine päriselu andmetes
- Andmete kvaliteedi hindamine ja äriline tõlgendus
- Meeskonnatöö efektiivsus andmeanalüüsis

## Failid
- Tiimi SQL päringud: `week1_task_a_sales.sql`, `week1_task_b_customers.sql`, `week1_task_c_products.sql`, 


## Järgmised sammud
- Andmete puhastamine ja valideerimine
- Sügavam analüüs müügikanalite lõikes
- Kliendiprofiilide loomine turunduse jaoks