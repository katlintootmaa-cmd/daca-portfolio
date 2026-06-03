# Nädal 2 tiimitöö: SQL Cleaning

English version: [README_EN.md](README_EN.md)

## Kokkuvõte

Nädal 2 keskendus andmekvaliteedile. Tiim otsis duplikaate, puuduvaid väärtusi, vigaseid kuupäevi, ebaloogilisi summasid ja tabelitevahelisi vastuolusid, et enne analüüsi oleks selge, kui usaldusväärsed UrbanStyle'i andmed on.

## Rollijaotus

| Roll | Tiimiliige | Ülesanne |
|------|------------|----------|
| A | Kätlin | Müügiandmete puhastamine: kontrollis `sales` tabeli duplikaate, kuupäevi, summasid ja tühje kliendiseoseid. |
| B | Ragnar | Kliendiandmete puhastamine: kontrollis `customers` tabeli puuduvaid väärtusi, e-posti/linna välju ja korduvaid kirjeid. |
| C | Karmo | Tooteandmete puhastamine: kontrollis `products` tabeli kategooriaid, hindu ja tootekoodide järjepidevust. |
| D | Mari | Ristvalideerimine ja kvaliteedikontroll: võrdles tabelite seoseid ning koondas kvaliteediriskid. |

## Rollide kirjeldused

- Roll A ehk müügiandmete puhastaja vastutas selle eest, et müügiridade summad, kuupäevad ja kliendiseosed oleksid analüüsiks kasutatavad. Rolli fookus oli vigaste või puudulike müügikirjete leidmisel.
- Roll B ehk kliendiandmete puhastaja vastutas kliendiinfo järjepidevuse eest. Roll kontrollis tühje välju, korduvaid kliente ja seda, kas kontakt- või asukohainfo sobib hilisemaks segmenteerimiseks.
- Roll C ehk tooteandmete puhastaja vastutas tootekataloogi kvaliteedi eest. Roll kontrollis hindu, kategooriaid ja tooteidentifikaatoreid, et toodete analüüs ei annaks eksitavaid tulemusi.
- Roll D ehk kvaliteedikontrolli koordinaator vaatas andmeid tabeliteüleselt. Rolli ülesanne oli leida seoseprobleeme, näiteks müük ilma kliendi või tooteta, ning koondada riskid ühisesse ülevaatesse.

## Peamised oskused

- `IS NULL`, `DISTINCT`, `COUNT`, `GROUP BY` ja tingimusfiltrite kasutamine kvaliteedikontrollis.
- Probleemsete kirjete leidmine enne analüüsi.
- Andmekvaliteedi mõju sõnastamine ärilises keeles.

## Väljund

Tiim koostas andmepuhastuse ülevaate, mis kirjeldab olulisemad kvaliteediprobleemid ja annab aluse järgmise nädala JOIN-analüüsiks.
