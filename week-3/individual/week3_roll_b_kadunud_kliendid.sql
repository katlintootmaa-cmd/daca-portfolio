-- Week 3, Roll B: kadunud kliendid
-- Eesmärk: leida UrbanStyle kliendid, kes on registreerunud,
-- aga kellel ei ole sales tabelis mitte ühtegi ostu.
-- PostgreSQL märkus: kasuta COUNT(*), mitte COUNT().

-- 1. Kadunud klientide nimekiri
-- LEFT JOIN toob kaasa kõik kliendid. Kui sales poolel vastet ei ole,
-- siis s.sale_id on NULL ja see tähendab, et klient pole ostnud.
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.city,
    c.registration_date,
    c.loyalty_tier,
    s.sale_id
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL
ORDER BY c.registration_date DESC, c.customer_id;

-- 2. Mitu kadunud klienti on?
SELECT
    COUNT(*) AS kadunud_kliente
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL;

-- 3. Kadunud klientide osakaal kõigist klientidest
SELECT
    COUNT(DISTINCT c.customer_id) AS koik_kliendid,
    COUNT(DISTINCT c.customer_id) FILTER (WHERE s.sale_id IS NULL) AS kadunud_kliente,
    ROUND(
        COUNT(DISTINCT c.customer_id) FILTER (WHERE s.sale_id IS NULL)::numeric
        / COUNT(DISTINCT c.customer_id) * 100,
        1
    ) AS kadunud_osakaal_protsent
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id;

-- 4. Kadunud kliendid linnade kaupa
SELECT
    COALESCE(NULLIF(TRIM(c.city), ''), 'teadmata') AS linn,
    COUNT(*) AS kadunud_kliente
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL
GROUP BY COALESCE(NULLIF(TRIM(c.city), ''), 'teadmata')
ORDER BY kadunud_kliente DESC, linn;

-- 5. Kadunud klientide registreerimise kuupäevad
SELECT
    c.first_name || ' ' || c.last_name AS klient,
    c.email,
    c.registration_date,
    c.city,
    COALESCE(c.loyalty_tier, 'puudub') AS loyalty_tier
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL
ORDER BY c.registration_date DESC, klient;

-- 6. Kadunud vs aktiivsed kliendid
-- COUNT(DISTINCT) on vajalik, sest aktiivsel kliendil võib olla mitu osturida.
SELECT
    CASE
        WHEN s.sale_id IS NULL THEN 'Kadunud (pole ostnud)'
        ELSE 'Aktiivne (on ostnud)'
    END AS staatus,
    COUNT(DISTINCT c.customer_id) AS kliente
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
GROUP BY
    CASE
        WHEN s.sale_id IS NULL THEN 'Kadunud (pole ostnud)'
        ELSE 'Aktiivne (on ostnud)'
    END
ORDER BY kliente DESC;

-- 7. Kadunud kliendid lojaalsustaseme järgi
SELECT
    COALESCE(c.loyalty_tier, 'puudub') AS loyalty_tier,
    COUNT(*) AS kadunud_kliente
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL
GROUP BY COALESCE(c.loyalty_tier, 'puudub')
ORDER BY kadunud_kliente DESC;

-- 8. Edasijõudnute tase: kadunud kliendid registreerimiskuu kaupa
SELECT
    DATE_TRUNC('month', c.registration_date)::date AS registreerimise_kuu,
    COUNT(*) AS kadunud_kliente
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL
GROUP BY DATE_TRUNC('month', c.registration_date)::date
ORDER BY registreerimise_kuu;

-- 9. Edasijõudnute tase: iga registreerimiskuu kadunud klientide osakaal
-- See aitab leida kuid, kus tuli palju registreerujaid, aga ostuni ei jõutud.
WITH kliendi_staatus AS (
    SELECT
        c.customer_id,
        DATE_TRUNC('month', c.registration_date)::date AS registreerimise_kuu,
        CASE
            WHEN COUNT(s.sale_id) = 0 THEN 1
            ELSE 0
        END AS on_kadunud
    FROM customers c
    LEFT JOIN sales s
        ON c.customer_id = s.customer_id
    GROUP BY
        c.customer_id,
        DATE_TRUNC('month', c.registration_date)::date
)
SELECT
    registreerimise_kuu,
    COUNT(*) AS registreerunud_kliente,
    SUM(on_kadunud) AS kadunud_kliente,
    ROUND(SUM(on_kadunud)::numeric / COUNT(*) * 100, 1) AS kadunud_osakaal_protsent
FROM kliendi_staatus
GROUP BY registreerimise_kuu
ORDER BY registreerimise_kuu;

-- 10. Praktiline kampaanianimekiri Annale
-- Värskeimad ostuta kliendid, kellele võiks saata esimese ostu pakkumise.
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS klient,
    c.email,
    c.city,
    c.registration_date,
    COALESCE(c.loyalty_tier, 'puudub') AS loyalty_tier,
    CASE
        WHEN c.registration_date >= DATE '2025-01-01' THEN '1. prioriteet: uus klient'
        WHEN c.registration_date >= DATE '2024-10-01' THEN '2. prioriteet: hiljutine klient'
        ELSE '3. prioriteet: vanem kontakt'
    END AS kampaania_prioriteet
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL
ORDER BY c.registration_date DESC, c.customer_id
LIMIT 50;

-- Raport Annale:
-- Andmete põhjal on UrbanStyle'il 599 klienti, kes pole kunagi ostnud.
-- See on 19,0% kõigist 3150 kliendist, seega ei ole tegu väikese kõrvalnähuga.
-- Kõige rohkem ostuta kliente on Tallinnas (231), Tartus (133) ja Pärnus (70).
-- Registreerimised jäävad vahemikku 2020-01-02 kuni 2025-02-27.
-- Suurim riskikoht on hiljutine periood: 2024. aastal registreerus 293 ostuta klienti
-- ja 2025. aasta alguses juba 100. Soovitus: teha eraldi esimese ostu kampaania
-- 2024 lõpu ja 2025 alguse klientidele, alustades Tallinnast, Tartust ja Pärnust.
