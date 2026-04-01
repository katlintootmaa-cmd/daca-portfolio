-- ALAÜLESANDE KAART A: Müügiandmed
-- Roll A: Müügiandmete uurija

-- 1. Mitu rida on sales tabelis?
SELECT COUNT(*) AS ridade_arv FROM sales;

-- 2. Millised veerud ja andmed tabelis on?
SELECT * FROM sales LIMIT 10;

-- 3. Tallinna kaupluse müügid
SELECT * FROM sales
WHERE store_location = 'Tallinn'
ORDER BY sale_date DESC
LIMIT 15;

-- 4. 10 suurimat tehingut
SELECT * FROM sales ORDER BY total_price DESC LIMIT 10;

-- 5. 10 väikseimat tehingut (kas on 0 või negatiivseid?)
SELECT * FROM sales ORDER BY total_price ASC LIMIT 10;

-- 6. Mitu rida, kus kliendi info on puudu?
SELECT COUNT(*) - COUNT(customer_id) AS puuduv_klient
FROM sales;

-- EDASIJÕUDNUTE TASE --

-- DISTINCT päring: Unikaalsed müügikanalid
SELECT DISTINCT channel FROM sales;

-- COUNT päring: Tehingute arv kaupluse kohta
SELECT store_location, COUNT(*) AS tehinguid
FROM sales
GROUP BY store_location
ORDER BY tehinguid DESC;

-- Kombineeritud tingimused: Tehingud üle 100 EUR Tallinnas
SELECT * FROM sales
WHERE total_price > 100 AND store_location = 'Tallinn'
ORDER BY total_price DESC;