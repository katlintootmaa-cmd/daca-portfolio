-- Week 4, Roll A: müügi koondandmed
-- Eesmärk:
-- 1. Koostada 2024. aasta kuine müügivaade.
-- 2. Leida tugevamad kategooriad GROUP BY + HAVING abil.
-- 3. Näidata kuust-kuusse trendi CTE ja LAG() abil.


-- 1. Müük kuude kaupa 2024
SELECT
    DATE_TRUNC('month', s.sale_date)::date AS kuu,
    COUNT(s.sale_id) AS tellimuste_arv,
    ROUND(SUM(s.total_price), 2) AS kogukaive,
    ROUND(AVG(s.total_price), 2) AS keskmine_tellimus
FROM sales s
WHERE s.sale_date >= DATE '2024-01-01'
  AND s.sale_date < DATE '2025-01-01'
GROUP BY DATE_TRUNC('month', s.sale_date)::date
ORDER BY kuu;


-- 2. Müük kategooriate kaupa 2024
-- Valitud HAVING piir: ainult kategooriad, mille kogumüük on üle 180000 euro.
SELECT
    p.category,
    COUNT(DISTINCT p.product_id) AS toodete_arv,
    ROUND(SUM(s.total_price), 2) AS kogumyyk,
    ROUND(AVG(s.unit_price), 2) AS keskmine_hind,
    SUM(s.quantity) AS myydud_yhikuid
FROM sales s
JOIN products p
    ON p.product_id = s.product_id
WHERE s.sale_date >= DATE '2024-01-01'
  AND s.sale_date < DATE '2025-01-01'
GROUP BY p.category
HAVING SUM(s.total_price) > 180000
ORDER BY kogumyyk DESC;


-- 3. Kuised trendid CTE + window function abil
WITH kuu_myyk AS (
    SELECT
        DATE_TRUNC('month', s.sale_date)::date AS kuu,
        SUM(s.total_price) AS kaive
    FROM sales s
    WHERE s.sale_date >= DATE '2024-01-01'
      AND s.sale_date < DATE '2025-01-01'
    GROUP BY DATE_TRUNC('month', s.sale_date)::date
)
SELECT
    kuu,
    ROUND(kaive, 2) AS kaive,
    ROUND(LAG(kaive) OVER (ORDER BY kuu), 2) AS eelmine_kuu,
    ROUND(kaive - LAG(kaive) OVER (ORDER BY kuu), 2) AS muutus_eurodes,
    ROUND(
        CASE
            WHEN LAG(kaive) OVER (ORDER BY kuu) IS NULL
              OR LAG(kaive) OVER (ORDER BY kuu) = 0
                THEN NULL
            ELSE (
                (kaive - LAG(kaive) OVER (ORDER BY kuu))
                / LAG(kaive) OVER (ORDER BY kuu)
            ) * 100
        END,
        1
    ) AS kasvu_protsent
FROM kuu_myyk
ORDER BY kuu;

-- Lühike tõlgendus:
-- 2024 tugevaim kuu on detsember, nõrgim kuu jaanuar.
-- Suurim käibehüpe toimub novembrist detsembrisse.
-- 2024. aasta käivet veavad peamiselt meeste_riided, jalanõusid ja naiste_riided.
