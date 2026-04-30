-- Nädal 2 - Roll C: tooteandmete puhastamine
-- PostgreSQL / Supabase
-- Käivita päringud järjekorras. Need muudavad ainult products_test tabelit, mitte products tabelit.
-- Selles skeemis vastab juhendi price veerule retail_price ja brand veerule supplier.

-- 1. Loo värske testkoopia.
DROP TABLE IF EXISTS products_test;

CREATE TABLE products_test AS
SELECT *
FROM products;

-- 2. Loe ridade arv enne puhastamist.
SELECT COUNT(*) AS ridade_arv
FROM products_test;

-- 3. Leia korduvad tootenimed.
SELECT
    product_name,
    COUNT(*) AS koopiate_arv
FROM products_test
GROUP BY product_name
HAVING COUNT(*) > 1
ORDER BY koopiate_arv DESC, product_name;

-- 4. Loe kokku duplikaatsete tootenimede grupid.
SELECT COUNT(*) AS duplikaatsed_tootenimed
FROM (
    SELECT product_name
    FROM products_test
    GROUP BY product_name
    HAVING COUNT(*) > 1
) d;

-- 5. Leia ka ühtlustatud tootenimede duplikaadid, sest tühikud ja suur-/väiketähed võivad duplikaate peita.
SELECT
    INITCAP(TRIM(product_name)) AS puhastatud_tootenimi,
    COUNT(*) AS koopiate_arv,
    COUNT(DISTINCT product_name) AS erinevaid_nimekujusid
FROM products_test
WHERE product_name IS NOT NULL
  AND TRIM(product_name) <> ''
GROUP BY INITCAP(TRIM(product_name))
HAVING COUNT(*) > 1
ORDER BY koopiate_arv DESC, puhastatud_tootenimi;

-- 6. Leia NULL väärtused olulistes väljades.
SELECT
    COUNT(*) FILTER (WHERE product_name IS NULL OR TRIM(product_name) = '') AS null_nimi,
    COUNT(*) FILTER (WHERE category IS NULL OR TRIM(category) = '') AS null_kategooria,
    COUNT(*) FILTER (WHERE retail_price IS NULL) AS null_hind,
    COUNT(*) FILTER (WHERE supplier IS NULL OR TRIM(supplier) = '') AS null_tarnija,
    COUNT(*) FILTER (WHERE subcategory IS NULL OR TRIM(subcategory) = '') AS null_alamkategooria,
    COUNT(*) FILTER (WHERE cost_price IS NULL) AS null_omahind
FROM products_test;

-- 7. Kontrolli loogilisi hinnavigu.
SELECT COUNT(*) AS negatiivne_hind
FROM products_test
WHERE retail_price < 0;

SELECT COUNT(*) AS negatiivne_omahind
FROM products_test
WHERE cost_price < 0;

SELECT COUNT(*) AS aarmuslik_hind
FROM products_test
WHERE retail_price > 1000;

SELECT
    product_id,
    product_name,
    retail_price
FROM products_test
WHERE retail_price > 1000
ORDER BY retail_price DESC;

SELECT COUNT(*) AS omahind_suurem_kui_jaehind
FROM products_test
WHERE cost_price > retail_price;

SELECT
    product_id,
    product_name,
    cost_price,
    retail_price,
    cost_price - retail_price AS erinevus
FROM products_test
WHERE cost_price > retail_price
ORDER BY erinevus DESC;

-- 8. Kontrolli kategooriate järjekindlust.
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
HAVING COUNT(DISTINCT category) > 1
ORDER BY erinevaid_kirjaviise DESC, tooteid DESC, puhastatud_kategooria;

-- 9. Kokkuvõte enne puhastamist raporti jaoks.
WITH duplicate_names AS (
    SELECT COUNT(*) AS cnt
    FROM (
        SELECT product_name
        FROM products_test
        GROUP BY product_name
        HAVING COUNT(*) > 1
    ) d
),
category_variants AS (
    SELECT COUNT(*) AS cnt
    FROM (
        SELECT INITCAP(REPLACE(TRIM(category), '_', ' ')) AS normalized_category
        FROM products_test
        WHERE category IS NOT NULL
          AND TRIM(category) <> ''
        GROUP BY INITCAP(REPLACE(TRIM(category), '_', ' '))
        HAVING COUNT(DISTINCT category) > 1
    ) c
),
quality_counts AS (
    SELECT
        COUNT(*) FILTER (WHERE product_name IS NULL OR TRIM(product_name) = '') AS null_nimi,
        COUNT(*) FILTER (WHERE category IS NULL OR TRIM(category) = '') AS null_kategooria,
        COUNT(*) FILTER (WHERE retail_price IS NULL) AS null_hind,
        COUNT(*) FILTER (WHERE supplier IS NULL OR TRIM(supplier) = '') AS null_tarnija,
        COUNT(*) FILTER (WHERE retail_price < 0 OR retail_price > 1000 OR cost_price > retail_price) AS loogilised_vead
    FROM products_test
)
SELECT 'duplikaatsed_nimed' AS kategooria, cnt AS leitud_probleeme
FROM duplicate_names
UNION ALL
SELECT 'null_nimi_hind', null_nimi + null_hind FROM quality_counts
UNION ALL
SELECT 'loogilised_vead', loogilised_vead FROM quality_counts
UNION ALL
SELECT 'ebajarjekindlad_kategooriad', cnt FROM category_variants
UNION ALL
SELECT 'null_tarnija_kategooria', null_tarnija + null_kategooria FROM quality_counts;

-- Edasijõudnute osa: puhasta testkoopia.
-- 10. Ühtlusta toodete tekstiväljad.
UPDATE products_test
SET
    product_name = NULLIF(INITCAP(TRIM(product_name)), ''),
    category = NULLIF(INITCAP(REPLACE(TRIM(category), '_', ' ')), ''),
    subcategory = NULLIF(INITCAP(REPLACE(TRIM(subcategory), '_', ' ')), ''),
    supplier = NULLIF(INITCAP(TRIM(supplier)), '');

-- 11. Ühtlusta levinud kategoorianimed CASE WHEN abil.
UPDATE products_test
SET category = CASE
    WHEN LOWER(TRIM(category)) IN ('shoes', 'footwear') OR LOWER(TRIM(category)) LIKE 'jalan%' THEN 'Shoes'
    WHEN LOWER(TRIM(category)) IN ('shirts', 'tops') OR LOWER(TRIM(category)) LIKE 'sark%' THEN 'Shirts'
    WHEN LOWER(TRIM(category)) IN ('pants', 'trousers') OR LOWER(TRIM(category)) LIKE 'puks%' THEN 'Pants'
    WHEN LOWER(TRIM(category)) IN ('women clothes', 'women clothing', 'naiste riided') THEN 'Naiste Riided'
    WHEN LOWER(TRIM(category)) IN ('men clothes', 'men clothing', 'meeste riided') THEN 'Meeste Riided'
    ELSE INITCAP(TRIM(category))
END
WHERE category IS NOT NULL;

-- 12. Muuda võimatud negatiivsed jaehinnad testkoopias NULL-iks.
UPDATE products_test
SET retail_price = NULL
WHERE retail_price < 0;

-- 13. Loe ridade arv pärast puhastamist.
SELECT COUNT(*) AS ridu_parast
FROM products_test;

-- 14. Lõpukontroll pärast puhastamist.
SELECT
    COUNT(*) FILTER (WHERE product_name IS NULL OR TRIM(product_name) = '') AS null_nimi,
    COUNT(*) FILTER (WHERE category IS NULL OR TRIM(category) = '') AS null_kategooria,
    COUNT(*) FILTER (WHERE retail_price IS NULL) AS null_hind,
    COUNT(*) FILTER (WHERE supplier IS NULL OR TRIM(supplier) = '') AS null_tarnija,
    COUNT(*) FILTER (WHERE retail_price < 0) AS negatiivne_hind,
    COUNT(*) FILTER (WHERE retail_price > 1000) AS aarmuslik_hind,
    COUNT(*) FILTER (WHERE cost_price > retail_price) AS omahind_suurem_kui_jaehind
FROM products_test;

SELECT
    category,
    COUNT(*) AS arv
FROM products_test
GROUP BY category
ORDER BY category;
