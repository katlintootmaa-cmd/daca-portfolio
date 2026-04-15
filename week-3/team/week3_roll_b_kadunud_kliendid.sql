-- Week 3, roll B: kadunud kliendid
-- Eesmärk: leida kliendid, kellel pole mitte ühtegi ostu.
-- Märkus: PostgreSQL-is tuleb kasutada COUNT(*), mitte COUNT().

-- 1. Leia kliendid, kellel pole ühtegi ostu.
-- LEFT JOIN tagab, et tulemusse tulevad ka kliendid, kellel müügirida puudub.
SELECT
    c.first_name,
    c.last_name,
    c.email,
    c.city,
    c.registration_date,
    s.sale_id
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL
ORDER BY c.registration_date DESC;

-- 2. Loe kokku, mitu "kadunud" klienti on.
SELECT
    COUNT(*) AS kadunud_kliente
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL;

-- 3. Analüüsi kadunud kliente linnade kaupa.
SELECT
    c.city,
    COUNT(*) AS kadunud_kliente
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL
GROUP BY c.city
ORDER BY kadunud_kliente DESC;

-- 4. Uuri registreerimise kuupäeva.
SELECT
    c.first_name || ' ' || c.last_name AS klient,
    c.registration_date,
    c.city,
    c.loyalty_tier
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL
ORDER BY c.registration_date DESC;

-- 5. Võrdle kadunud vs aktiivsete klientide arvu.
-- Kasutame COUNT(DISTINCT c.customer_id), sest aktiivsel kliendil võib olla mitu osturida.
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

-- 6. Lisa: kadunud kliendid registreerimisaasta järgi.
SELECT
    EXTRACT(YEAR FROM c.registration_date)::int AS registreerimise_aasta,
    COUNT(*) AS kadunud_kliente
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL
GROUP BY EXTRACT(YEAR FROM c.registration_date)::int
ORDER BY registreerimise_aasta;

-- 7. Lisa: kadunud kliendid registreerimiskuu järgi.
SELECT
    TO_CHAR(c.registration_date, 'YYYY-MM') AS registreerimise_kuu,
    COUNT(*) AS kadunud_kliente
FROM customers c
LEFT JOIN sales s
    ON c.customer_id = s.customer_id
WHERE s.sale_id IS NULL
GROUP BY TO_CHAR(c.registration_date, 'YYYY-MM')
ORDER BY registreerimise_kuu DESC;

-- 8. Lisa: registreerimisaja analüüs koos osakaaluga.
-- See näitab, kas kadunud kliendid on pigem vanad või uued registreerujad.
WITH kliendi_staatus AS (
    SELECT
        c.customer_id,
        c.registration_date,
        CASE
            WHEN COUNT(s.sale_id) = 0 THEN 1
            ELSE 0
        END AS on_kadunud
    FROM customers c
    LEFT JOIN sales s
        ON c.customer_id = s.customer_id
    GROUP BY c.customer_id, c.registration_date
)
SELECT
    EXTRACT(YEAR FROM registration_date)::int AS registreerimise_aasta,
    COUNT(*) AS registreerunud_kliente,
    SUM(on_kadunud) AS kadunud_kliente,
    ROUND(SUM(on_kadunud)::numeric / COUNT(*) * 100, 1) AS kadunud_osakaal_protsent
FROM kliendi_staatus
GROUP BY EXTRACT(YEAR FROM registration_date)::int
ORDER BY registreerimise_aasta;

-- 9. Raport Annale:
-- Anna, päringu järgi on meil 599 klienti, kes pole kunagi ostnud.
-- Neid on kõigis linnades, kõige rohkem Tallinnas (231), Tartus (133) ja Pärnus (70).
-- Registreerimised jäävad vahemikku 2020-01-02 kuni 2025-02-27, kuid suurim osa on väga värsked kliendid: 2024 registreerus neist 293 ja 2025 alguses juba 100.
-- Soovitan teha neile eraldi esimese ostu kampaania, alustades 2024 lõpu ja 2025 alguse klientidest, näiteks personaalse sooduskoodi, tasuta tarne või linnapõhise pakkumisega Tallinnale, Tartule ja Pärnule.
