
 <img width="934" height="420" alt="image" src="https://github.com/user-attachments/assets/f8e9c52e-18a3-43f5-8c0b-73ffcdf3e39a" />


## Andmete puhastamise kokkuvõte

Andmete valideerimise käigus tuvastati järgmised probleemid:
- 5 116 duplikaatset rida
- 1 487 puuduvat `customer_id` väärtust  
- 9 vigast tulevikukuupäeva

### Teostatud puhastamistoimingud:
- Eemaldati duplikaatsed read
- Asendati puuduvad kliendi viited väärtusega "Tundmatu klient"
- Parandati vigased kuupäevad

### Tulemused:
- Pärast puhastamist jäi tabelisse 10 118 korrektset rida
- Selle tulemusena said aruanded täpsemaks ja usaldusväärsemaks ning vähenes risk teha valesid ärilisi otsuseid.
