-- ALAÜLESANDE KAART C: Tooteandmed
-- Roll C: Tooteandmete uurija

-- 1. Mitu toodet on kokku?
SELECT COUNT(*) AS toodete_arv FROM products;

-- 2. Millised veerud ja andmed tabelis on?
SELECT * FROM products LIMIT 10;

-- 3. Kõik unikaalsed tootekategooriad
SELECT DISTINCT category FROM products;

-- 4. 10 kallemat toodet
SELECT product_name, category, retail_price
FROM products
ORDER BY retail_price DESC
LIMIT 10;

-- 10 odavamat toodet
SELECT product_name, category, retail_price
FROM products
ORDER BY retail_price ASC
LIMIT 10;

-- 5. Näide: kõik kindla kategooria tooted
SELECT * FROM products
WHERE category = 'Kleidid'
ORDER BY retail_price DESC;

-- 6. Puuduvad andmed
SELECT COUNT(*) - COUNT(retail_price) AS puuduvad_hinnad
FROM products;

SELECT COUNT(*) - COUNT(category) AS puuduvad_kategooriad
FROM products;

-- EDASIJÕUDNUTE TASE --

-- Loe tooted kategooriati kokku
SELECT category, COUNT(*) AS toodete_arv
FROM products
GROUP BY category
ORDER BY toodete_arv DESC;

-- Keskmised hinnad kategooriati
SELECT category,
       COUNT(*) AS toodete_arv,
       MIN(retail_price) AS min_hind,
       MAX(retail_price) AS max_hind
FROM products
GROUP BY category
ORDER BY max_hind DESC;

-- Kombineeri tingimused: Tooted üle 50 EUR kindlas kategoorias
SELECT * FROM products
WHERE retail_price > 50 AND category = 'Kleidid'
ORDER BY retail_price DESC;