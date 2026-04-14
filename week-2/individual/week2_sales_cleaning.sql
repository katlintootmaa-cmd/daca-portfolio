-- Nädal 2 - Roll A: müügiandmete puhastamine
-- PostgreSQL / Supabase
-- Käivita päringud järjekorras. Need muudavad ainult sales_test tabelit, mitte sales tabelit.

-- 1. Loo värske testkoopia.
DROP TABLE IF EXISTS sales_test;

CREATE TABLE sales_test AS
SELECT *
FROM sales;

-- 2. Loe ridade arv enne puhastamist.
SELECT COUNT(*) AS ridade_arv
FROM sales_test;

-- 3. Leia korduvad sale_id väärtused.
SELECT
    sale_id,
    COUNT(*) AS koopiate_arv
FROM sales_test
GROUP BY sale_id
HAVING COUNT(*) > 1
ORDER BY koopiate_arv DESC, sale_id;

-- 4. Loe kokku üleliigsed duplikaatread.
-- Juhendis kasutatakse id veergu, aga selles skeemis on sale_id ja eraldi id veergu ei ole.
-- ctid aitab testkoopias füüsilisi ridu eristada.
WITH ranked_sales AS (
    SELECT
        ctid,
        sale_id,
        ROW_NUMBER() OVER (
            PARTITION BY sale_id
            ORDER BY sale_date, invoice_id, product_id, customer_id NULLS LAST, ctid
        ) AS rn
    FROM sales_test
)
SELECT COUNT(*) AS duplikaat_read
FROM ranked_sales
WHERE rn > 1;

-- 5. Leia NULL väärtused olulistes väljades.
SELECT
    COUNT(*) FILTER (WHERE customer_id IS NULL) AS null_customer_id,
    COUNT(*) FILTER (WHERE sale_date IS NULL) AS null_sale_date,
    COUNT(*) FILTER (WHERE total_price IS NULL) AS null_total_price,
    COUNT(*) FILTER (WHERE product_id IS NULL) AS null_product_id,
    COUNT(*) FILTER (WHERE quantity IS NULL) AS null_quantity,
    COUNT(*) FILTER (WHERE unit_price IS NULL) AS null_unit_price,
    COUNT(*) FILTER (WHERE invoice_id IS NULL OR TRIM(invoice_id) = '') AS null_invoice_id,
    COUNT(*) FILTER (WHERE channel IS NULL OR TRIM(channel) = '') AS null_channel,
    COUNT(*) FILTER (WHERE payment_method IS NULL OR TRIM(payment_method) = '') AS null_payment_method
FROM sales_test;

-- 6. Kontrolli tuleviku kuupäevi.
SELECT COUNT(*) AS tuleviku_kuupaevad
FROM sales_test
WHERE sale_date > CURRENT_DATE;

-- 7. Lisakontrollid raporti jaoks.
SELECT
    COUNT(*) FILTER (WHERE quantity <= 0) AS vigane_kogus,
    COUNT(*) FILTER (WHERE unit_price < 0) AS negatiivne_uhikuhind,
    COUNT(*) FILTER (WHERE total_price < 0) AS negatiivne_kogusumma,
    COUNT(*) FILTER (WHERE total_price IS NOT NULL
                     AND quantity IS NOT NULL
                     AND unit_price IS NOT NULL
                     AND ABS(total_price - quantity * unit_price) > 1) AS summa_ei_klapi
FROM sales_test;

-- 8. Kuva dokumenteerimiseks probleemsete ridade näited.
SELECT
    sale_id,
    invoice_id,
    sale_date,
    customer_id,
    product_id,
    quantity,
    unit_price,
    total_price
FROM sales_test
WHERE customer_id IS NULL
   OR sale_date IS NULL
   OR total_price IS NULL
   OR sale_date > CURRENT_DATE
   OR quantity <= 0
   OR unit_price < 0
   OR total_price < 0
ORDER BY sale_id
LIMIT 50;

-- 9. Kokkuvõte enne puhastamist raporti jaoks.
WITH duplicate_rows AS (
    SELECT COUNT(*) AS cnt
    FROM (
        SELECT
            ROW_NUMBER() OVER (
                PARTITION BY sale_id
                ORDER BY sale_date, invoice_id, product_id, customer_id NULLS LAST, ctid
            ) AS rn
        FROM sales_test
    ) x
    WHERE rn > 1
),
quality_counts AS (
    SELECT
        COUNT(*) FILTER (WHERE customer_id IS NULL) AS null_customer_id,
        COUNT(*) FILTER (WHERE sale_date IS NULL) AS null_sale_date,
        COUNT(*) FILTER (WHERE total_price IS NULL) AS null_total_price,
        COUNT(*) FILTER (WHERE sale_date > CURRENT_DATE) AS tuleviku_kuupaevad
    FROM sales_test
)
SELECT 'duplikaat_read' AS kategooria, cnt AS leitud_probleeme
FROM duplicate_rows
UNION ALL
SELECT 'null_customer_id', null_customer_id FROM quality_counts
UNION ALL
SELECT 'null_sale_date', null_sale_date FROM quality_counts
UNION ALL
SELECT 'null_total_price', null_total_price FROM quality_counts
UNION ALL
SELECT 'tuleviku_kuupaevad', tuleviku_kuupaevad FROM quality_counts;

-- Edasijõudnute osa: puhasta testkoopia.
-- 10. Kustuta duplikaatread ja jäta alles esimene rida iga sale_id kohta.
WITH ranked_sales AS (
    SELECT
        ctid,
        ROW_NUMBER() OVER (
            PARTITION BY sale_id
            ORDER BY sale_date, invoice_id, product_id, customer_id NULLS LAST, ctid
        ) AS rn
    FROM sales_test
)
DELETE FROM sales_test s
USING ranked_sales r
WHERE s.ctid = r.ctid
  AND r.rn > 1;

-- 11. Asenda NULL customer_id väärtus ainult testkoopias väärtusega 0.
-- Ära käivita sama UPDATE päringut sales tabelil: sales.customer_id viitab customers tabelile
-- ja selles skeemis tähendab NULL külalisostjat.
UPDATE sales_test
SET customer_id = 0
WHERE customer_id IS NULL;

-- 12. Paranda tuleviku kuupäevad testkoopias.
UPDATE sales_test
SET sale_date = CURRENT_DATE
WHERE sale_date > CURRENT_DATE;

-- 13. Arvuta puuduv total_price uuesti, kui quantity ja unit_price on olemas.
UPDATE sales_test
SET total_price = quantity * unit_price
WHERE total_price IS NULL
  AND quantity IS NOT NULL
  AND unit_price IS NOT NULL;

-- 14. Ühtlusta tekstiväljad.
UPDATE sales_test
SET
    invoice_id = NULLIF(TRIM(invoice_id), ''),
    channel = NULLIF(LOWER(TRIM(channel)), ''),
    store_location = NULLIF(INITCAP(TRIM(store_location)), ''),
    payment_method = NULLIF(LOWER(TRIM(payment_method)), '');

-- 15. Loe ridade arv pärast puhastamist.
SELECT COUNT(*) AS ridu_parast
FROM sales_test;

-- 16. Lõpukontroll pärast puhastamist.
SELECT
    COUNT(*) FILTER (WHERE customer_id IS NULL) AS null_customer_id,
    COUNT(*) FILTER (WHERE sale_date IS NULL) AS null_sale_date,
    COUNT(*) FILTER (WHERE total_price IS NULL) AS null_total_price,
    COUNT(*) FILTER (WHERE sale_date > CURRENT_DATE) AS tuleviku_kuupaevad
FROM sales_test;

SELECT
    sale_id,
    COUNT(*) AS koopiate_arv
FROM sales_test
GROUP BY sale_id
HAVING COUNT(*) > 1
ORDER BY koopiate_arv DESC, sale_id;
