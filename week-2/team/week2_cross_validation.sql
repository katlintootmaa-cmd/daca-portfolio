-- Nädal 2 - Roll D: ristvalideerimine ja kvaliteedikontroll
-- PostgreSQL / Supabase
-- Need päringud loevad sales, customers ja products tabeleid. Andmeid ei muudeta.
-- Selles skeemis vastab juhendi toote hinna veerule products.retail_price.

-- 1. Kontrolli, kas kõik sales tabelis olevad customer_id väärtused eksisteerivad customers tabelis.
SELECT COUNT(*) AS orb_klient
FROM sales s
LEFT JOIN customers c
    ON s.customer_id = c.customer_id
WHERE c.customer_id IS NULL
  AND s.customer_id IS NOT NULL;

-- Kuva näidisread puuduvate kliendiviidetega.
SELECT
    s.sale_id,
    s.invoice_id,
    s.customer_id,
    s.product_id,
    s.sale_date,
    s.total_price
FROM sales s
LEFT JOIN customers c
    ON s.customer_id = c.customer_id
WHERE c.customer_id IS NULL
  AND s.customer_id IS NOT NULL
ORDER BY s.sale_id
LIMIT 50;

-- 2. Kontrolli, kas kõik sales tabelis olevad product_id väärtused eksisteerivad products tabelis.
SELECT COUNT(*) AS orb_toode
FROM sales s
LEFT JOIN products p
    ON s.product_id = p.product_id
WHERE p.product_id IS NULL
  AND s.product_id IS NOT NULL;

-- Kuva näidisread puuduvate tooteviidetega.
SELECT
    s.sale_id,
    s.invoice_id,
    s.customer_id,
    s.product_id,
    s.sale_date,
    s.total_price
FROM sales s
LEFT JOIN products p
    ON s.product_id = p.product_id
WHERE p.product_id IS NULL
  AND s.product_id IS NOT NULL
ORDER BY s.sale_id
LIMIT 50;

-- 3. Kontrolli, kas müügihind klapib toote hinna ja kogusega.
SELECT
    s.sale_id,
    s.total_price,
    p.retail_price AS tootehind,
    s.quantity,
    s.total_price - (p.retail_price * s.quantity) AS erinevus
FROM sales s
JOIN products p
    ON s.product_id = p.product_id
WHERE ABS(s.total_price - (p.retail_price * s.quantity)) > 1
ORDER BY ABS(s.total_price - (p.retail_price * s.quantity)) DESC
LIMIT 20;

-- Loe kokku hinna ebakõlad.
SELECT COUNT(*) AS hinna_ebakolad
FROM sales s
JOIN products p
    ON s.product_id = p.product_id
WHERE ABS(s.total_price - (p.retail_price * s.quantity)) > 1;

-- Lisakontroll: unit_price peaks klappima products.retail_price väärtusega.
SELECT COUNT(*) AS uhikuhinna_ebakolad
FROM sales s
JOIN products p
    ON s.product_id = p.product_id
WHERE ABS(s.unit_price - p.retail_price) > 1;

-- 4. Kontrolli kliente, kes pole kunagi ostnud.
SELECT COUNT(*) AS vaimkliendid
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.customer_id IS NULL;

-- Kuva näited klientidest, kes pole kunagi ostnud.
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.city
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.customer_id IS NULL
ORDER BY c.customer_id
LIMIT 50;

-- 5. Kontrolli tooteid, mida pole kunagi müüdud.
SELECT COUNT(*) AS vaimtooted
FROM products p
LEFT JOIN sales s
    ON p.product_id = s.product_id
WHERE s.product_id IS NULL;

-- Kuva näited toodetest, mida pole kunagi müüdud.
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.retail_price
FROM products p
LEFT JOIN sales s
    ON p.product_id = s.product_id
WHERE s.product_id IS NULL
ORDER BY p.product_id
LIMIT 50;

-- 6. Ristvalideerimise kokkuvõte raporti jaoks.
SELECT 'orb_klient' AS kategooria, COUNT(*) AS leitud_probleeme
FROM sales s
LEFT JOIN customers c
    ON s.customer_id = c.customer_id
WHERE c.customer_id IS NULL
  AND s.customer_id IS NOT NULL
UNION ALL
SELECT 'orb_toode', COUNT(*)
FROM sales s
LEFT JOIN products p
    ON s.product_id = p.product_id
WHERE p.product_id IS NULL
  AND s.product_id IS NOT NULL
UNION ALL
SELECT 'hinna_ebakolad', COUNT(*)
FROM sales s
JOIN products p
    ON s.product_id = p.product_id
WHERE ABS(s.total_price - (p.retail_price * s.quantity)) > 1
UNION ALL
SELECT 'vaimkliendid', COUNT(*)
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.customer_id IS NULL
UNION ALL
SELECT 'vaimtooted', COUNT(*)
FROM products p
LEFT JOIN sales s
    ON p.product_id = s.product_id
WHERE s.product_id IS NULL;

-- Edasijõudnute osa: millistel toodetel on kõige suuremad hinnaerinevused?
SELECT
    p.product_name,
    p.category,
    p.retail_price AS list_hind,
    AVG(s.total_price / NULLIF(s.quantity, 0)) AS kesk_muugihind,
    p.retail_price - AVG(s.total_price / NULLIF(s.quantity, 0)) AS erinevus
FROM products p
JOIN sales s
    ON p.product_id = s.product_id
GROUP BY p.product_id, p.product_name, p.category, p.retail_price
HAVING ABS(p.retail_price - AVG(s.total_price / NULLIF(s.quantity, 0))) > 5
ORDER BY ABS(p.retail_price - AVG(s.total_price / NULLIF(s.quantity, 0))) DESC
LIMIT 10;
