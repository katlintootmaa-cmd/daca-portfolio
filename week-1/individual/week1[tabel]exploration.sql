-- Roll D: Müügikanalite uurija

-- 1. Millised kanalid, asukohad ja makseviisid on?
SELECT channel, store_location, payment_method
FROM sales
LIMIT 10;

-- 2. Unikaalsed müügikanalid
SELECT DISTINCT channel FROM sales;

-- 3. Unikaalsed kaupluste asukohad
SELECT DISTINCT store_location FROM sales;


-- 4. Unikaalsed makseviisid
SELECT DISTINCT payment_method FROM sales;

-- 5. Online-müügid
SELECT * FROM sales
WHERE channel = 'online'
ORDER BY total_price DESC
LIMIT 15;

-- 6. Tehingud ilma kaupluse asukohata
SELECT COUNT(*) AS puuduv_asukoht
FROM sales
WHERE store_location IS NULL;

-- EDASIJÕUDNUTE TASE --

-- Loe tehingud kokku iga kaupluse asukoha kohta
SELECT store_location, COUNT(*) AS tehinguid
FROM sales
WHERE store_location IS NOT NULL
ORDER BY tehinguid DESC;

-- Võrdle online vs pood tehingute arvu
-- Online-tehingute arv
SELECT COUNT(*) AS online_tehinguid
FROM sales
WHERE channel = 'online';

-- Poe-tehingute arv
SELECT COUNT(*) AS poe_tehinguid
FROM sales
WHERE channel = 'pood';

-- Kombineeri tingimused: Sularahamaksed Tartus
SELECT * FROM sales
WHERE payment_method = 'sularaha'
  AND store_location = 'Tartu'
ORDER BY total_price DESC
LIMIT 10;