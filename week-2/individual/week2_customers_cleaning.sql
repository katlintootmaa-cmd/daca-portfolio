-- Week 2 - Roll B
-- Customer Data Cleaner
-- Eesmärk: leida customers tabelist duplikaadid, puuduvad väärtused
-- ja ebajärjekindlad nimekujud ohutult testkoopial.

-- Samm 1. Loo testkoopia
CREATE TABLE customers_test AS
SELECT *
FROM customers;

-- Kontrolli ridade arvu
SELECT COUNT(*) AS ridade_arv
FROM customers_test;

-- Samm 2. Leia duplikaatsed e-mailid
SELECT
    email,
    COUNT(*) AS koopiate_arv
FROM customers_test
WHERE email IS NOT NULL
  AND TRIM(email) <> ''
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY koopiate_arv DESC, email;

-- Samm 3. Leia puuduvad nimed
SELECT
    COUNT(*) FILTER (WHERE first_name IS NULL OR TRIM(first_name) = '') AS null_eesnimi,
    COUNT(*) FILTER (WHERE last_name IS NULL OR TRIM(last_name) = '') AS null_perenimi
FROM customers_test;

-- Samm 4. Kontrolli linnade ebajärjekindlat kirjapilti
SELECT
    city AS originaal_linn,
    TRIM(city) AS trimmitud_linn,
    INITCAP(TRIM(city)) AS puhastatud_linn,
    COUNT(*) AS kliendid
FROM customers_test
GROUP BY city
ORDER BY city;

-- Sama linna erinevate nimekujude kokkuvõte
SELECT
    INITCAP(TRIM(city)) AS puhastatud_linn,
    COUNT(*) AS kliente_kokku,
    COUNT(DISTINCT city) AS erinevaid_kirjaviise
FROM customers_test
WHERE city IS NOT NULL
  AND TRIM(city) <> ''
GROUP BY INITCAP(TRIM(city))
ORDER BY kliente_kokku DESC, puhastatud_linn;

-- Samm 5. Kontrolli kontaktandmete puudumist
SELECT
    COUNT(*) FILTER (WHERE phone IS NULL OR TRIM(phone) = '') AS null_telefon,
    COUNT(*) FILTER (WHERE email IS NULL OR TRIM(email) = '') AS null_email
FROM customers_test;

-- Näita puudulike andmetega kliendid
SELECT
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    city
FROM customers_test
WHERE first_name IS NULL
   OR TRIM(first_name) = ''
   OR last_name IS NULL
   OR TRIM(last_name) = ''
   OR email IS NULL
   OR TRIM(email) = ''
   OR phone IS NULL
   OR TRIM(phone) = ''
ORDER BY customer_id
LIMIT 50;

-- Roll B kokkuvõttepäring raporti jaoks
SELECT
    COUNT(*) FILTER (WHERE email IS NOT NULL AND TRIM(email) <> '') AS email_olemas,
    COUNT(*) FILTER (WHERE email IS NULL OR TRIM(email) = '') AS email_puudub,
    COUNT(*) FILTER (WHERE first_name IS NULL OR TRIM(first_name) = '') AS eesnimi_puudub,
    COUNT(*) FILTER (WHERE last_name IS NULL OR TRIM(last_name) = '') AS perenimi_puudub,
    COUNT(*) FILTER (WHERE phone IS NULL OR TRIM(phone) = '') AS telefon_puudub
FROM customers_test;
