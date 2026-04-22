-- Week 4, Roll B: kliendigruppide analüüs
-- Eesmärk:
-- 1. Segmenteerida kliendid kulutuse järgi.
-- 2. Leida TOP 10 kõige väärtuslikumat klienti.
-- 3. Näidata segmentide jaotus linnade lõikes.
--
-- Valitud segmendipiirid:
-- VIP     >= 1500 eurot kogukäivet
-- Regular >= 700 eurot kogukäivet
-- Uus     < 700 eurot kogukäivet


-- 1. Kliendigruppide analüüs CTE-ga
WITH kliendi_kokkuvote AS (
    SELECT
        c.customer_id,
        c.first_name || ' ' || c.last_name AS nimi,
        c.city,
        COUNT(s.sale_id) AS tellimuste_arv,
        ROUND(SUM(s.total_price), 2) AS kogukaive
    FROM customers c
    JOIN sales s
        ON s.customer_id = c.customer_id
    GROUP BY
        c.customer_id,
        c.first_name,
        c.last_name,
        c.city
)
SELECT
    customer_id,
    nimi,
    city,
    tellimuste_arv,
    kogukaive,
    CASE
        WHEN kogukaive >= 1500 THEN 'VIP'
        WHEN kogukaive >= 700 THEN 'Regular'
        ELSE 'Uus'
    END AS segment
FROM kliendi_kokkuvote
ORDER BY kogukaive DESC, tellimuste_arv DESC;


-- 2. TOP 10 klienti
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS nimi,
    c.city,
    COUNT(s.sale_id) AS tellimuste_arv,
    ROUND(SUM(s.total_price), 2) AS kogukaive
FROM customers c
JOIN sales s
    ON s.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city
HAVING COUNT(s.sale_id) >= 2
ORDER BY kogukaive DESC
LIMIT 10;


-- 3. Segmentide koondstatistika linnade kaupa
-- RANK() näitab, millistes linnades on igas segmendis suurim kliendibaas.
WITH kliendi_kokkuvote AS (
    SELECT
        c.customer_id,
        c.city,
        ROUND(SUM(s.total_price), 2) AS kogukaive
    FROM customers c
    JOIN sales s
        ON s.customer_id = c.customer_id
    GROUP BY
        c.customer_id,
        c.city
),
segmendid AS (
    SELECT
        customer_id,
        city,
        kogukaive,
        CASE
            WHEN kogukaive >= 1500 THEN 'VIP'
            WHEN kogukaive >= 700 THEN 'Regular'
            ELSE 'Uus'
        END AS segment
    FROM kliendi_kokkuvote
)
SELECT
    segment,
    city,
    COUNT(*) AS kliente,
    ROUND(AVG(kogukaive), 2) AS keskmine_kaive,
    RANK() OVER (
        PARTITION BY segment
        ORDER BY COUNT(*) DESC, AVG(kogukaive) DESC
    ) AS koht_segmendis
FROM segmendid
GROUP BY
    segment,
    city
ORDER BY
    segment,
    koht_segmendis,
    city;

-- Lühike tõlgendus:
-- VIP-kliente on vähem, aga nende keskmine käive on kordades kõrgem.
-- Tallinnas ja Tartus on suurim VIP-klientide baas.
-- TOP-kliendid väärivad eraldi hoidmis- ja lojaalsusstrateegiat.
