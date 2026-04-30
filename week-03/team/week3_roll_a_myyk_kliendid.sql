-- Week 3, Roll A: myyk + kliendid
-- Eesmärk: ühendada sales ja customers INNER JOIN-iga,
-- et leida ostnud kliendid, TOP kliendid ja müügi jaotus.

-- 1. Lihtne INNER JOIN: kliendid, kes on ostnud
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.email,
    c.city,
    s.sale_id,
    s.sale_date,
    s.total_price
FROM sales s
INNER JOIN customers c
    ON s.customer_id = c.customer_id
ORDER BY s.sale_date DESC
LIMIT 20;

-- 2. TOP 10 klienti kogumüügi järgi
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS klient,
    c.city,
    COUNT(DISTINCT s.sale_id) AS ostude_arv,
    ROUND(SUM(s.total_price), 2) AS kogumyyk
FROM sales s
INNER JOIN customers c
    ON s.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city
ORDER BY kogumyyk DESC
LIMIT 10;

-- 3. Müük linnade kaupa
SELECT
    COALESCE(NULLIF(TRIM(c.city), ''), 'teadmata') AS linn,
    COUNT(DISTINCT c.customer_id) AS kliente,
    COUNT(s.sale_id) AS oste,
    ROUND(SUM(s.total_price), 2) AS kogumyyk,
    ROUND(AVG(s.total_price), 2) AS keskmine_ost
FROM sales s
INNER JOIN customers c
    ON s.customer_id = c.customer_id
GROUP BY COALESCE(NULLIF(TRIM(c.city), ''), 'teadmata')
ORDER BY kogumyyk DESC;

-- 4. Müük lojaalsustasemete kaupa
SELECT
    COALESCE(c.loyalty_tier, 'puudub') AS loyalty_tier,
    COUNT(DISTINCT c.customer_id) AS kliente,
    COUNT(s.sale_id) AS oste,
    ROUND(SUM(s.total_price), 2) AS kogumyyk,
    ROUND(AVG(s.total_price), 2) AS keskmine_ost
FROM sales s
INNER JOIN customers c
    ON s.customer_id = c.customer_id
GROUP BY COALESCE(c.loyalty_tier, 'puudub')
ORDER BY kogumyyk DESC;

-- 5. Edasijõudnute tase: kliendid, kelle kogumüük on üle keskmise kliendimüügi
WITH kliendi_myyk AS (
    SELECT
        c.customer_id,
        c.first_name || ' ' || c.last_name AS klient,
        c.city,
        SUM(s.total_price) AS kogumyyk
    FROM sales s
    INNER JOIN customers c
        ON s.customer_id = c.customer_id
    GROUP BY
        c.customer_id,
        c.first_name,
        c.last_name,
        c.city
),
keskmine AS (
    SELECT AVG(kogumyyk) AS keskmine_kliendi_myyk
    FROM kliendi_myyk
)
SELECT
    km.customer_id,
    km.klient,
    km.city,
    ROUND(km.kogumyyk, 2) AS kogumyyk,
    ROUND(k.keskmine_kliendi_myyk, 2) AS keskmine_kliendi_myyk
FROM kliendi_myyk km
CROSS JOIN keskmine k
WHERE km.kogumyyk > k.keskmine_kliendi_myyk
ORDER BY km.kogumyyk DESC;

-- 6. Kui suur osa ostnud klientidest on üle keskmise kulutajad?
WITH kliendi_myyk AS (
    SELECT
        c.customer_id,
        SUM(s.total_price) AS kogumyyk
    FROM sales s
    INNER JOIN customers c
        ON s.customer_id = c.customer_id
    GROUP BY c.customer_id
),
keskmine AS (
    SELECT AVG(kogumyyk) AS keskmine_kliendi_myyk
    FROM kliendi_myyk
)
SELECT
    COUNT(*) AS ostnud_kliente,
    COUNT(*) FILTER (WHERE km.kogumyyk > k.keskmine_kliendi_myyk) AS yle_keskmise_kliente,
    ROUND(
        COUNT(*) FILTER (WHERE km.kogumyyk > k.keskmine_kliendi_myyk)::numeric
        / COUNT(*) * 100,
        1
    ) AS yle_keskmise_osakaal_protsent
FROM kliendi_myyk km
CROSS JOIN keskmine k;

-- Kokkuvõte Annale:
-- Parim klient on Tiina Pärn Tartust: 73 ostu ja 27668.02 eurot kogumüüki.
-- TOP 3 klienti on Tiina Pärn, Priit Rand ja Kevin Org.
-- Linnadest toob kõige rohkem müüki Tallinn: 1006252.88 eurot, 1007 klienti ja 3601 ostu.
-- Lojaalsustasemetest annab suurima kogumüügi grupp "puudub": 1071805.32 eurot.
-- Soovitus: hoida TOP-kliente personaalse pakkumisega ning uurida, miks suurima käibega kliendid
-- ei ole alati loyalty_tier süsteemis selgelt märgitud.
