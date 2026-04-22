-- Nädal 2 - Roll B: kliendiandmete puhastamine
-- PostgreSQL / Supabase
-- Käivita päringud järjekorras. Need muudavad ainult customers_test tabelit, mitte customers tabelit.

-- 1. Loo värske testkoopia.
DROP TABLE IF EXISTS customers_test;

CREATE TABLE customers_test AS
SELECT *
FROM customers;

-- 2. Loe ridade arv enne puhastamist.
SELECT COUNT(*) AS ridade_arv
FROM customers_test;

-- 3. Leia korduvad e-posti aadressid.
SELECT
    LOWER(TRIM(email)) AS email,
    COUNT(*) AS koopiate_arv
FROM customers_test
WHERE email IS NOT NULL
  AND TRIM(email) <> ''
GROUP BY LOWER(TRIM(email))
HAVING COUNT(*) > 1
ORDER BY koopiate_arv DESC, email;

-- 4. Loe kokku duplikaatsete e-posti aadresside grupid.
SELECT COUNT(*) AS duplikaatsed_emailid
FROM (
    SELECT LOWER(TRIM(email)) AS normalized_email
    FROM customers_test
    WHERE email IS NOT NULL
      AND TRIM(email) <> ''
    GROUP BY LOWER(TRIM(email))
    HAVING COUNT(*) > 1
) d;

-- 5. Kuva korduvate e-posti aadressidega kliendikirjed.
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    city,
    registration_date,
    loyalty_tier
FROM customers_test
WHERE LOWER(TRIM(email)) IN (
    SELECT LOWER(TRIM(email))
    FROM customers_test
    WHERE email IS NOT NULL
      AND TRIM(email) <> ''
    GROUP BY LOWER(TRIM(email))
    HAVING COUNT(*) > 1
)
ORDER BY LOWER(TRIM(email)), customer_id
LIMIT 100;

-- 6. Leia puuduvad nimed.
SELECT
    COUNT(*) FILTER (WHERE first_name IS NULL OR TRIM(first_name) = '') AS null_eesnimi,
    COUNT(*) FILTER (WHERE last_name IS NULL OR TRIM(last_name) = '') AS null_perenimi
FROM customers_test;

-- 7. Kontrolli linnanimede erinevaid kirjapilte.
SELECT
    city,
    COUNT(*) AS arv
FROM customers_test
GROUP BY city
ORDER BY city;

-- 8. Loe kokku ühtlustatud linnanimede erinevad nimekujud.
SELECT
    INITCAP(TRIM(city)) AS puhastatud_linn,
    COUNT(*) AS kliendid,
    COUNT(DISTINCT city) AS erinevaid_nimekujusid
FROM customers_test
WHERE city IS NOT NULL
  AND TRIM(city) <> ''
GROUP BY INITCAP(TRIM(city))
HAVING COUNT(DISTINCT city) > 1
ORDER BY erinevaid_nimekujusid DESC, kliendid DESC, puhastatud_linn;

-- 9. Kontrolli puuduvaid kontaktandmeid.
SELECT
    COUNT(*) FILTER (WHERE phone IS NULL OR TRIM(phone) = '') AS null_telefon,
    COUNT(*) FILTER (WHERE email IS NULL OR TRIM(email) = '') AS null_email
FROM customers_test;

-- 10. Lisakontrollid raporti jaoks.
SELECT
    COUNT(*) FILTER (WHERE city IS NULL OR TRIM(city) = '') AS null_linn,
    COUNT(*) FILTER (WHERE loyalty_tier IS NULL OR TRIM(loyalty_tier) = '') AS null_lojaalsustase,
    COUNT(*) FILTER (WHERE registration_date > CURRENT_DATE) AS tuleviku_registreerimine,
    COUNT(*) FILTER (WHERE birth_year < 1940 OR birth_year > 2010) AS vigane_synniaasta
FROM customers_test;

-- 11. Kontrolli lojaalsustasemete kirjapilti.
SELECT
    COALESCE(NULLIF(LOWER(TRIM(loyalty_tier)), ''), 'puudub') AS lojaalsustase,
    COUNT(*) AS kliendid
FROM customers_test
GROUP BY COALESCE(NULLIF(LOWER(TRIM(loyalty_tier)), ''), 'puudub')
ORDER BY kliendid DESC, lojaalsustase;

-- 12. Kokkuvõte enne puhastamist raporti jaoks.
WITH duplicate_emails AS (
    SELECT COUNT(*) AS cnt
    FROM (
        SELECT LOWER(TRIM(email)) AS normalized_email
        FROM customers_test
        WHERE email IS NOT NULL
          AND TRIM(email) <> ''
        GROUP BY LOWER(TRIM(email))
        HAVING COUNT(*) > 1
    ) d
),
city_variants AS (
    SELECT COUNT(*) AS cnt
    FROM (
        SELECT INITCAP(TRIM(city)) AS normalized_city
        FROM customers_test
        WHERE city IS NOT NULL
          AND TRIM(city) <> ''
        GROUP BY INITCAP(TRIM(city))
        HAVING COUNT(DISTINCT city) > 1
    ) c
),
quality_counts AS (
    SELECT
        COUNT(*) FILTER (WHERE first_name IS NULL OR TRIM(first_name) = '') AS null_eesnimi,
        COUNT(*) FILTER (WHERE last_name IS NULL OR TRIM(last_name) = '') AS null_perenimi,
        COUNT(*) FILTER (WHERE phone IS NULL OR TRIM(phone) = '') AS null_telefon,
        COUNT(*) FILTER (WHERE email IS NULL OR TRIM(email) = '') AS null_email
    FROM customers_test
)
SELECT 'duplikaatsed_emailid' AS kategooria, cnt AS leitud_probleeme
FROM duplicate_emails
UNION ALL
SELECT 'null_eesnimi', null_eesnimi FROM quality_counts
UNION ALL
SELECT 'null_perenimi', null_perenimi FROM quality_counts
UNION ALL
SELECT 'ebajarjekindlad_linnad', cnt FROM city_variants
UNION ALL
SELECT 'null_telefon_voi_email', null_telefon + null_email FROM quality_counts;

-- Edasijõudnute osa: puhasta testkoopia.
-- 13. Muuda tühjad stringid NULL-iks ja ühtlusta tekstiväljad.
UPDATE customers_test
SET
    first_name = NULLIF(INITCAP(TRIM(first_name)), ''),
    last_name = NULLIF(INITCAP(TRIM(last_name)), ''),
    email = NULLIF(LOWER(TRIM(email)), ''),
    phone = NULLIF(TRIM(phone), ''),
    city = NULLIF(INITCAP(TRIM(city)), ''),
    loyalty_tier = NULLIF(LOWER(TRIM(loyalty_tier)), '');

-- 14. Asenda puuduvad nimed.
UPDATE customers_test
SET first_name = 'Tundmatu'
WHERE first_name IS NULL;

UPDATE customers_test
SET last_name = 'Tundmatu'
WHERE last_name IS NULL;

-- 15. Jäta alles ainult lubatud lojaalsustaseme väärtused.
UPDATE customers_test
SET loyalty_tier = NULL
WHERE loyalty_tier IS NOT NULL
  AND loyalty_tier NOT IN ('bronze', 'silver', 'gold');

-- 16. Ühtlusta telefoninumbrid levinud Eesti vormingute jaoks.
UPDATE customers_test
SET phone = CASE
    WHEN phone IS NULL OR TRIM(phone) = '' THEN NULL
    WHEN REGEXP_REPLACE(phone, '[^0-9+]', '', 'g') LIKE '+372%' THEN REGEXP_REPLACE(phone, '[^0-9+]', '', 'g')
    WHEN REGEXP_REPLACE(phone, '[^0-9]', '', 'g') LIKE '372%' THEN '+' || REGEXP_REPLACE(phone, '[^0-9]', '', 'g')
    WHEN LENGTH(REGEXP_REPLACE(phone, '[^0-9]', '', 'g')) IN (7, 8) THEN '+372' || REGEXP_REPLACE(phone, '[^0-9]', '', 'g')
    ELSE REGEXP_REPLACE(phone, '\s+', ' ', 'g')
END;

-- 17. Eemalda korduva e-postiga read testkoopiast.
-- Alles jääb väikseima customer_id väärtusega rida iga e-posti aadressi kohta.
WITH ranked_customers AS (
    SELECT
        customer_id,
        ROW_NUMBER() OVER (
            PARTITION BY email
            ORDER BY customer_id
        ) AS rn
    FROM customers_test
    WHERE email IS NOT NULL
)
DELETE FROM customers_test c
USING ranked_customers r
WHERE c.customer_id = r.customer_id
  AND r.rn > 1;

-- 18. Loe ridade arv pärast puhastamist.
SELECT COUNT(*) AS ridu_parast
FROM customers_test;

-- 19. Lõpukontroll pärast puhastamist.
SELECT
    COUNT(*) FILTER (WHERE first_name IS NULL OR TRIM(first_name) = '') AS null_eesnimi,
    COUNT(*) FILTER (WHERE last_name IS NULL OR TRIM(last_name) = '') AS null_perenimi,
    COUNT(*) FILTER (WHERE phone IS NULL OR TRIM(phone) = '') AS null_telefon,
    COUNT(*) FILTER (WHERE email IS NULL OR TRIM(email) = '') AS null_email
FROM customers_test;

SELECT
    email,
    COUNT(*) AS koopiate_arv
FROM customers_test
WHERE email IS NOT NULL
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY koopiate_arv DESC, email;

SELECT
    city,
    COUNT(*) AS arv
FROM customers_test
GROUP BY city
ORDER BY city;

-- 20. CASE WHEN näide raporti jaoks.
SELECT
    phone,
    CASE
        WHEN phone LIKE '+372%' THEN phone
        WHEN phone LIKE '372%' THEN '+' || phone
        WHEN LENGTH(phone) = 7 THEN '+372' || phone
        ELSE phone
    END AS standardne_telefon
FROM customers_test
WHERE phone IS NOT NULL
LIMIT 10;
