# Nädal 7: Python Pandas - RFM kliendisegmenteerimine

## Minu roll

Roll B: Data Cleaning. Minu ülesanne oli võtta Roll A liidetud müügi- ja kliendiandmete DataFrame, eemaldada duplikaadid, käsitleda kriitilised NULL väärtused, parsida kuupäevad ning eemaldada vigased või mittepositiivsed `total_price` väärtused.

## Peamised leiud

- Puhastuse käigus on kõige olulisem kaitsta RFM analüüsi sisendit: `customer_id`, `sale_date` ja `total_price` ei tohi olla tühjad, sest nendest arvutatakse Recency, Frequency ja Monetary väärtused.
- Supabase andmetel jäi pärast puhastust alles 8950 müügirida ja 2540 unikaalset klienti.
- VIP Champions segment annab suurima osa käibest, kuigi see ei ole kõige suurem kliendigrupp.

## AI kasutamine

Kasutasin AI abi juhendi tõlgendamiseks, Roll B puhastusvoo koostamiseks ja tiimitöö notebooki Supabase-põhiseks muutmiseks. AI aitas lisada kontrollid, raportid ja ekspordi nii, et notebook järgib grupitöö juhendit.

## Failid

- `individual/week7_rfm_B.ipynb` - minu individuaalne Roll B notebook.
- `team/week7_rfm_complete.ipynb` - terviklik tiimitöö notebook rollidega A, B, C ja D.
- `team/rfm_segments.csv` - eksporditud kliendisegmendid.
