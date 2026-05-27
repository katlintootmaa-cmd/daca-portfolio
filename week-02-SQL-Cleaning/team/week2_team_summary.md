# Meeskonna koondraport - Nädal 2

## Andmekvaliteedi koondraport

## Peamised leiud
1. **Müügiandmed**: leitud 5509 probleemi. Duplikaadid ja `NULL` väärtused moonutavad müügiaruandeid.
2. **Kliendiandmed**: leitud 9 probleemi. Ebajärjekindlad linnanimed ja puuduvad e-mailid vähendavad andmete usaldusväärsust.
3. **Tooteandmed**: leitud 0 probleemi. Andmed on suhteliselt puhtad.
4. **Ristvalideerimine**: leitud 27580 probleemi. Esineb suur hulk orbeid ja vaimkirjeid.

## Suurim üllatus
Kõige suurem üllatus oli ristvalideerimise tulemus, kus peaaegu kõik müügid viitavad olematutele klientidele ja toodetele. See viitab sügavale andmebaasi struktuuri probleemile.

## Soovitus Toomasele
Esimesena tuleb lahendada duplikaadid müügiandmetes ja ristvalideerimise probleemid, et tagada andmete terviklikkus enne juhatuse koosolekut. Järgmised sammud on standardiseerimine ja puuduvate viidete lisamine.

## Puuduvad andmed
Me ei teadnud enne kontrolli, et müügiandmed ei ole üldse seotud klientide ja toodetega. See tähendab, et puuduvad õiged välisvõtmed või on andmed genereeritud eraldi.

## Kokkuvõte
Andmete puhastamine näitas, et UrbanStyle'i andmebaasis on tõsised kvaliteediprobleemid, eriti müügiandmetes ja ristvalideerimises. Detailsete leidude põhjal tuvastati kokku 33 098 probleemi, mis võivad moonutada ärilisi aruandeid. Soovitus on alustada duplikaatide eemaldamisest ja andmete ühendamisest, et tagada usaldusväärsus enne juhatuse koosolekut.
