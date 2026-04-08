-- Week 2 - Roll C
-- Product Data Cleaner
-- Eesmärk: kontrollida products tabelit duplikaatide, puuduvate väärtuste
-- ja loogiliste vigade suhtes testkoopial.

-- Samm 1. Loo testkoopia
CREATE TABLE products_test AS
SELECT *
FROM products;

-- Kontrolli ridade arvu
SELECT COUNT(*) AS ridade_arv
FROM products_test;

-- Samm 2. Leia võimalikud duplikaatsed tootenimed
SELECT
    product_name,
    COUNT(*) AS koopiate_arv
FROM products_test
GROUP BY product_name
HAVING COUNT(*) > 1
ORDER BY koopiate_arv DESC, product_name;

-- Vajadusel täpsem kontroll nime + kategooria järgi
SELECT
    product_name,
    category,
    COUNT(*) AS koopiate_arv
FROM products_test
GROUP BY product_name, category
HAVING COUNT(*) > 1
ORDER BY koopiate_arv DESC, product_name, category;

-- Samm 3. Leia puuduvad väärtused kriitilistes väljades
SELECT
    COUNT(*) FILTER (WHERE product_name IS NULL OR TRIM(product_name) = '') AS null_nimi,
    COUNT(*) FILTER (WHERE category IS NULL OR TRIM(category) = '') AS null_kategooria,
    COUNT(*) FILTER (WHERE subcategory IS NULL OR TRIM(subcategory) = '') AS null_alamkategooria,
    COUNT(*) FILTER (WHERE retail_price IS NULL) AS null_jaehind,
    COUNT(*) FILTER (WHERE cost_price IS NULL) AS null_omahind,
    COUNT(*) FILTER (WHERE supplier IS NULL OR TRIM(supplier) = '') AS null_tarnija
FROM products_test;

-- Samm 4. Kontrolli loogilisi hinnavigu
SELECT COUNT(*) AS negatiivne_jaehind
FROM products_test
WHERE retail_price < 0;

SELECT COUNT(*) AS negatiivne_omahind
FROM products_test
WHERE cost_price < 0;

SELECT
    product_id,
    product_name,
    cost_price,
    retail_price
FROM products_test
WHERE retail_price > 1000
ORDER BY retail_price DESC;

SELECT
    product_id,
    product_name,
    cost_price,
    retail_price
FROM products_test
WHERE cost_price > retail_price
ORDER BY cost_price - retail_price DESC;

-- Samm 5. Kontrolli kategooriate järjekindlust
SELECT
    category,
    COUNT(*) AS arv
FROM products_test
GROUP BY category
ORDER BY category;

SELECT
    INITCAP(REPLACE(TRIM(category), '_', ' ')) AS puhastatud_kategooria,
    COUNT(*) AS tooteid,
    COUNT(DISTINCT category) AS erinevaid_kirjaviise
FROM products_test
WHERE category IS NOT NULL
  AND TRIM(category) <> ''
GROUP BY INITCAP(REPLACE(TRIM(category), '_', ' '))
ORDER BY tooteid DESC, puhastatud_kategooria;

-- Roll C kokkuvõttepäring raporti jaoks
SELECT
    COUNT(*) FILTER (WHERE product_name IS NULL OR TRIM(product_name) = '') AS nimi_puudub,
    COUNT(*) FILTER (WHERE category IS NULL OR TRIM(category) = '') AS kategooria_puudub,
    COUNT(*) FILTER (WHERE retail_price < 0) AS negatiivne_jaehind,
    COUNT(*) FILTER (WHERE cost_price < 0) AS negatiivne_omahind,
    COUNT(*) FILTER (WHERE cost_price > retail_price) AS omahind_suurem_kui_jaehind
FROM products_test;
