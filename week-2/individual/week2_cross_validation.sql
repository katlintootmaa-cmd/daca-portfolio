-- Week 2 - Roll D
-- Cross Validation and Data Quality
-- Eesmärk: kontrollida tabelitevahelist terviklikkust customers, products
-- ja sales tabelite vahel.

-- Samm 1. Kontrolli, kas kõik müügis viidatud kliendid eksisteerivad
SELECT
    COUNT(*) AS orb_klient
FROM sales s
LEFT JOIN customers c
    ON s.customer_id = c.customer_id
WHERE s.customer_id IS NOT NULL
  AND c.customer_id IS NULL;

-- Näita näidisread puuduvate klientidega
SELECT
    s.sale_id,
    s.customer_id,
    s.product_id,
    s.sale_date,
    s.total_price
FROM sales s
LEFT JOIN customers c
    ON s.customer_id = c.customer_id
WHERE s.customer_id IS NOT NULL
  AND c.customer_id IS NULL
ORDER BY s.sale_id
LIMIT 50;

-- Samm 2. Kontrolli, kas kõik müügis viidatud tooted eksisteerivad
SELECT
    COUNT(*) AS orb_toode
FROM sales s
LEFT JOIN products p
    ON s.product_id = p.product_id
WHERE s.product_id IS NOT NULL
  AND p.product_id IS NULL;

-- Näita näidisread puuduvate toodetega
SELECT
    s.sale_id,
    s.customer_id,
    s.product_id,
    s.sale_date,
    s.total_price
FROM sales s
LEFT JOIN products p
    ON s.product_id = p.product_id
WHERE s.product_id IS NOT NULL
  AND p.product_id IS NULL
ORDER BY s.sale_id
LIMIT 50;

-- Samm 3. Kontrolli hindade kooskõla
SELECT
    s.sale_id,
    s.product_id,
    s.quantity,
    s.unit_price,
    p.retail_price AS toote_jaehind,
    s.total_price,
    s.quantity * s.unit_price AS arvutatud_summa,
    s.unit_price - p.retail_price AS uhikuhinna_erinevus,
    s.total_price - (s.quantity * s.unit_price) AS kogusumma_erinevus
FROM sales s
JOIN products p
    ON s.product_id = p.product_id
WHERE ABS(s.unit_price - p.retail_price) > 1
   OR ABS(s.total_price - (s.quantity * s.unit_price)) > 1
ORDER BY ABS(s.total_price - (s.quantity * s.unit_price)) DESC
LIMIT 50;

-- Kokkuvõte hinnakontrollist
SELECT
    COUNT(*) AS hinnaga_mitteklappivaid_muuge
FROM sales s
JOIN products p
    ON s.product_id = p.product_id
WHERE ABS(s.unit_price - p.retail_price) > 1
   OR ABS(s.total_price - (s.quantity * s.unit_price)) > 1;

-- Samm 4. Kontrolli, kas on kliente, kes pole kunagi ostnud
SELECT
    COUNT(*) AS vaimkliendid
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.customer_id IS NULL;

-- Samm 5. Kontrolli, kas on tooteid, mida pole kunagi müüdud
SELECT
    COUNT(*) AS vaimtooted
FROM products p
LEFT JOIN sales s
    ON p.product_id = s.product_id
WHERE s.product_id IS NULL;

-- Roll D kokkuvõttepäring raporti jaoks
SELECT 'orb_klient' AS probleem, COUNT(*) AS kirjete_arv
FROM sales s
LEFT JOIN customers c
    ON s.customer_id = c.customer_id
WHERE s.customer_id IS NOT NULL
  AND c.customer_id IS NULL
UNION ALL
SELECT 'orb_toode' AS probleem, COUNT(*) AS kirjete_arv
FROM sales s
LEFT JOIN products p
    ON s.product_id = p.product_id
WHERE s.product_id IS NOT NULL
  AND p.product_id IS NULL
UNION ALL
SELECT 'hinnakontrolli_vead' AS probleem, COUNT(*) AS kirjete_arv
FROM sales s
JOIN products p
    ON s.product_id = p.product_id
WHERE ABS(s.unit_price - p.retail_price) > 1
   OR ABS(s.total_price - (s.quantity * s.unit_price)) > 1
UNION ALL
SELECT 'vaimkliendid' AS probleem, COUNT(*) AS kirjete_arv
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.customer_id IS NULL
UNION ALL
SELECT 'vaimtooted' AS probleem, COUNT(*) AS kirjete_arv
FROM products p
LEFT JOIN sales s
    ON p.product_id = s.product_id
WHERE s.product_id IS NULL;
