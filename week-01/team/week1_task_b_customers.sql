-- ALAÜLESANDE KAART B: Kliendiandmed
-- Roll B: Kliendiandmete uurija

-- 1. Mitu klienti on kokku?
SELECT COUNT(*) AS klientide_arv FROM customers;

-- 2. Millised veerud ja andmed tabelis on?
SELECT * FROM customers LIMIT 10;

-- 3. Millised linnad on esindatud?
SELECT DISTINCT city FROM customers;

-- 4. Tallinna kliendid, sorteeritud nime järgi
SELECT * FROM customers
WHERE city = 'Tallinn'
ORDER BY last_name ASC
LIMIT 15;

-- 5. Vanim ja uusim registreerimine
SELECT MIN(registration_date) AS vanim,
       MAX(registration_date) AS uusim
FROM customers;

-- 6. Puuduvad andmed
SELECT COUNT(*) - COUNT(first_name) AS puuduvad_eesnimed
FROM customers;

SELECT COUNT(*) - COUNT(email) AS puuduvad_emailid
FROM customers;

-- EDASIJÕUDNUTE TASE --

-- Duplikaatsed e-mailid
SELECT COUNT(*) AS kokku_emaile,
       COUNT(DISTINCT email) AS unikaalseid_emaile
FROM customers;
-- Vahe = duplikaadid!

-- Kliendid linniti kokku
SELECT city, COUNT(*) AS klientide_arv
FROM customers
GROUP BY city
ORDER BY klientide_arv DESC;

-- Uued kliendid (viimase 6 kuu registreerimised)
SELECT * FROM customers
WHERE registration_date >= '2024-07-01'
ORDER BY registration_date DESC;