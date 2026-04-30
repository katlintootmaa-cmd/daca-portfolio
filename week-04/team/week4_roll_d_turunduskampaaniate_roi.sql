-- Week 4, Roll D: turunduskampaaniate ROI
-- Eesmärk:
-- 1. Koondada turunduskanalite tulemused.
-- 2. Arvutada kanali efektiivsus CTE-de abil.
-- 3. Näidata kuised kanalitrendid koos eelmise kuu võrdlusega.
--
-- NB! Kohalikus repos ei ole web_logs CSV eksporti, kuid skeem eeldab tabelit
-- web_logs. Need päringud on valmis käivitamiseks andmebaasis, kus see tabel
-- on olemas. Kasutan customer_source CTE-d, et vältida müükide duplitseerimist
-- olukorras, kus ühel kliendil on mitu veebikülastuse rida.


-- 1. Turunduskanalite koondandmed
WITH customer_source AS (
    SELECT
        w.customer_id,
        COALESCE(w.source, 'teadmata') AS turunduskanal,
        ROW_NUMBER() OVER (
            PARTITION BY w.customer_id
            ORDER BY w.visit_date DESC
        ) AS rn
    FROM web_logs w
    WHERE w.customer_id IS NOT NULL
)
SELECT
    cs.turunduskanal,
    COUNT(DISTINCT s.customer_id) AS kliente,
    COUNT(DISTINCT s.sale_id) AS tellimusi,
    ROUND(SUM(s.total_price), 2) AS kogukaive,
    ROUND(AVG(s.total_price), 2) AS keskmine_tellimus
FROM sales s
JOIN customers c
    ON c.customer_id = s.customer_id
LEFT JOIN customer_source cs
    ON cs.customer_id = c.customer_id
   AND cs.rn = 1
GROUP BY cs.turunduskanal
ORDER BY kogukaive DESC;


-- 2. Kanali efektiivsus CTE-ga
WITH customer_source AS (
    SELECT
        w.customer_id,
        COALESCE(w.source, 'teadmata') AS turunduskanal,
        ROW_NUMBER() OVER (
            PARTITION BY w.customer_id
            ORDER BY w.visit_date DESC
        ) AS rn
    FROM web_logs w
    WHERE w.customer_id IS NOT NULL
),
kanali_myyk AS (
    SELECT
        cs.turunduskanal,
        COUNT(DISTINCT s.sale_id) AS tellimusi,
        ROUND(SUM(s.total_price), 2) AS kogukaive
    FROM sales s
    LEFT JOIN customer_source cs
        ON cs.customer_id = s.customer_id
       AND cs.rn = 1
    GROUP BY cs.turunduskanal
    HAVING COUNT(DISTINCT s.sale_id) > 100
),
kanali_kliendid AS (
    SELECT
        cs.turunduskanal,
        COUNT(DISTINCT cs.customer_id) AS kliente
    FROM customer_source cs
    WHERE cs.rn = 1
    GROUP BY cs.turunduskanal
)
SELECT
    km.turunduskanal,
    km.tellimusi,
    kk.kliente,
    km.kogukaive,
    ROUND(km.kogukaive / NULLIF(kk.kliente, 0), 2) AS kaive_kliendi_kohta,
    ROUND(km.kogukaive / NULLIF(km.tellimusi, 0), 2) AS kaive_tellimuse_kohta
FROM kanali_myyk km
LEFT JOIN kanali_kliendid kk
    ON kk.turunduskanal = km.turunduskanal
ORDER BY kaive_kliendi_kohta DESC, kogukaive DESC;


-- 3. Kampaaniate kuised trendid
WITH customer_source AS (
    SELECT
        w.customer_id,
        COALESCE(w.source, 'teadmata') AS turunduskanal,
        ROW_NUMBER() OVER (
            PARTITION BY w.customer_id
            ORDER BY w.visit_date DESC
        ) AS rn
    FROM web_logs w
    WHERE w.customer_id IS NOT NULL
),
kuu_kanal AS (
    SELECT
        cs.turunduskanal,
        DATE_TRUNC('month', s.sale_date)::date AS kuu,
        COUNT(DISTINCT s.sale_id) AS tellimusi,
        COUNT(DISTINCT s.customer_id) AS kliente,
        SUM(s.total_price) AS kogukaive
    FROM sales s
    LEFT JOIN customer_source cs
        ON cs.customer_id = s.customer_id
       AND cs.rn = 1
    GROUP BY
        cs.turunduskanal,
        DATE_TRUNC('month', s.sale_date)::date
    HAVING COUNT(DISTINCT s.sale_id) > 20
)
SELECT
    turunduskanal,
    kuu,
    tellimusi,
    kliente,
    ROUND(kogukaive, 2) AS kogukaive,
    ROUND(LAG(kogukaive) OVER (
        PARTITION BY turunduskanal
        ORDER BY kuu
    ), 2) AS eelmise_kuu_kaive,
    ROUND(
        kogukaive - LAG(kogukaive) OVER (
            PARTITION BY turunduskanal
            ORDER BY kuu
        ),
        2
    ) AS muutus_eurodes
FROM kuu_kanal
ORDER BY kuu, kogukaive DESC;

-- Lühike tõlgendus:
-- Kui web_logs on laaditud, saab Kristi jaoks välja tuua 3-5 kanalipõhist koondnumbrit.
-- Kui mõnel kliendil puudub source, kuvatakse kanalina "teadmata".
-- See on oluline äriline signaal: atribuutika ei pruugi olla täielik.
