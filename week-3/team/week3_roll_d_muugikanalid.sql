-- Week 3, Roll D: müügikanalid + kliendid + tooted
-- Eesmärk: võrrelda müügikanaleid ning ühendada sales, customers ja products.

-- 1. Millised müügikanalid on sales tabelis olemas?
SELECT DISTINCT
    s.channel
FROM sales s
ORDER BY s.channel;

-- 2. Kanalite põhiülevaade
SELECT
    s.channel AS myygikanal,
    COUNT(DISTINCT s.customer_id) AS kliente,
    COUNT(s.sale_id) AS oste,
    ROUND(SUM(s.total_price), 2) AS kogumyyk,
    ROUND(AVG(s.total_price), 2) AS keskmine_ost
FROM sales s
GROUP BY s.channel
ORDER BY kogumyyk DESC;

-- 3. Millistest linnadest kliendid milliseid kanaleid kasutavad?
SELECT
    s.channel AS myygikanal,
    COALESCE(NULLIF(TRIM(c.city), ''), 'teadmata') AS linn,
    COUNT(DISTINCT c.customer_id) AS kliente,
    COUNT(s.sale_id) AS oste,
    ROUND(SUM(s.total_price), 2) AS kogumyyk
FROM sales s
INNER JOIN customers c
    ON s.customer_id = c.customer_id
GROUP BY
    s.channel,
    COALESCE(NULLIF(TRIM(c.city), ''), 'teadmata')
ORDER BY
    s.channel,
    kogumyyk DESC;

-- 4. 3 tabeli JOIN: millised tootekategooriad müüvad millises kanalis?
SELECT
    s.channel AS myygikanal,
    p.category AS tootekategooria,
    COUNT(DISTINCT c.customer_id) AS kliente,
    COUNT(s.sale_id) AS oste,
    ROUND(SUM(s.total_price), 2) AS kogumyyk,
    ROUND(AVG(s.total_price), 2) AS keskmine_ost
FROM sales s
INNER JOIN customers c
    ON s.customer_id = c.customer_id
INNER JOIN products p
    ON s.product_id = p.product_id
GROUP BY
    s.channel,
    p.category
ORDER BY
    s.channel,
    kogumyyk DESC;

-- 5. Kõige efektiivsem kanal: müük ühe kliendi kohta
SELECT
    s.channel AS myygikanal,
    COUNT(DISTINCT s.customer_id) AS kliente,
    COUNT(s.sale_id) AS oste,
    ROUND(SUM(s.total_price), 2) AS kogumyyk,
    ROUND(SUM(s.total_price) / COUNT(DISTINCT s.customer_id), 2) AS myyk_per_klient
FROM sales s
WHERE s.customer_id IS NOT NULL
GROUP BY s.channel
ORDER BY myyk_per_klient DESC;

-- 6. Kaupluste ja kanalite võrdlus
SELECT
    COALESCE(s.store_location, 'online') AS kauplus,
    s.channel AS myygikanal,
    COUNT(s.sale_id) AS oste,
    ROUND(SUM(s.total_price), 2) AS kogumyyk,
    ROUND(AVG(s.total_price), 2) AS keskmine_ost
FROM sales s
GROUP BY
    COALESCE(s.store_location, 'online'),
    s.channel
ORDER BY
    kauplus,
    kogumyyk DESC;

-- 7. Kanalid lojaalsustasemete järgi
SELECT
    s.channel AS myygikanal,
    COALESCE(c.loyalty_tier, 'puudub') AS loyalty_tier,
    COUNT(DISTINCT c.customer_id) AS kliente,
    COUNT(s.sale_id) AS oste,
    ROUND(SUM(s.total_price), 2) AS kogumyyk
FROM sales s
INNER JOIN customers c
    ON s.customer_id = c.customer_id
GROUP BY
    s.channel,
    COALESCE(c.loyalty_tier, 'puudub')
ORDER BY
    s.channel,
    kogumyyk DESC;

-- Kokkuvõte Annale:
-- Sales tabelis on kaks kanalit: pood ja online.
-- Pood toob suurema kogumüügi: 1902430.30 eurot, 6656 ostu ja 2278 klienti.
-- Online kanal annab 1006747.68 eurot, 3462 ostu ja 1706 klienti.
-- Müük ühe kliendi kohta on samuti parem poes: 835.13 eurot vs online 590.12 eurot.
-- Mõlemas kanalis on tugevaim kategooria "jalanõusid"; linnadest domineerib Tallinn.
-- Soovitus: hoida poodide tugevust, aga kasvatada online-kanali konversiooni,
-- sest online toob palju kliente, kuid väiksema müügi ühe kliendi kohta.
