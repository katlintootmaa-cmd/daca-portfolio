-- Sales Data cleaner

-- Samm 1. Loo testkoopia
CREATE TABLE sales_test AS
SELECT * FROM sales;

-- Kontrolli ridade arvu
SELECT COUNT(*) AS ridade_arv
FROM sales_test;

-- Samm 2. Leia duplikaatsed tellimused
SELECT sale_id, COUNT(*) AS koopiate_arv
FROM sales_test
GROUP BY sale_id
HAVING COUNT(*) > 1
ORDER BY koopiate_arv DESC;

-- Samm 3. Loe kokku duplikaatsed read
SELECT COUNT(*) AS duplikaat_read
FROM sales_test
WHERE id NOT IN (
    SELECT MIN(id)
    FROM sales_test
    GROUP BY sale_id
);

-- Samm 4. Leia NULL väärtused kriitilistes väljades
SELECT
    COUNT(*) FILTER (WHERE customer_id IS NULL) AS null_customer_id,
    COUNT(*) FILTER (WHERE sale_date IS NULL) AS null_sale_date,
    COUNT(*) FILTER (WHERE total_price IS NULL) AS null_total_price
FROM sales_test;

-- Samm 5. Kontrolli tuleviku kuupäevi
SELECT COUNT(*) AS tuleviku_kuupaevad
FROM sales_test
WHERE sale_date > CURRENT_DATE;

-- Duplikaatide kustutamine: alles jääb ainult väikseima id-ga rida iga sale_id kohta
DELETE FROM sales_test
WHERE id NOT IN (
    SELECT MIN(id)
    FROM sales_test
    GROUP BY sale_id
);

-- NULL customer_id asendamine
UPDATE sales_test
SET customer_id = 0
WHERE customer_id IS NULL;

-- Tuleviku kuupäevade parandamine
UPDATE sales_test
SET sale_date = CURRENT_DATE
WHERE sale_date > CURRENT_DATE;

-- Kontroll: mitu rida jäi alles
SELECT COUNT(*) AS ridu_parast
FROM sales_test;

-- Lisakontroll pärast puhastamist
SELECT sale_id, COUNT(*) AS koopiate_arv
FROM sales_test
GROUP BY sale_id
HAVING COUNT(*) > 1;

SELECT
    COUNT(*) FILTER (WHERE customer_id IS NULL) AS null_customer_id,
    COUNT(*) FILTER (WHERE sale_date IS NULL) AS null_sale_date,
    COUNT(*) FILTER (WHERE total_price IS NULL) AS null_total_price
FROM sales_test;

SELECT COUNT(*) AS tuleviku_kuupaevad
FROM sales_test
WHERE sale_date > CURRENT_DATE;