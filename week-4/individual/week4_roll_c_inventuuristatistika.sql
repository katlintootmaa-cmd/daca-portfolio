-- Week 4, Roll C: inventuuristatistika
-- Eesmärk:
-- 1. Võrrelda tootekategooriate hindu ja mahtu.
-- 2. Leida müüdud vs laos suhted kategooriate lõikes.
-- 3. Järjestada tooted kategooria sees window function abil.
-- 4. Koostada kokkuvõtlik kategooriaraport koos soovitustega.
--
-- NB! Tööjuhendis on kirjas inventorymovements, kuid selle projekti skeemis
-- on tabeli nimi inventory_movements. Hetkelaoseisu jaoks kasutan inventory
-- tabelit, sest seal on olemas quantity_available.


-- 1. Tootekategooriate koondandmed
-- COUNT(DISTINCT product_id) ja COUNT(product_id) annavad siin sama tulemuse,
-- sest products tabelis on iga toode ainult ühel real.
-- Pärast JOIN-e ei pruugi see enam kehtida, sest sama product_id võib korduda.
SELECT
    p.category,
    COUNT(DISTINCT p.product_id) AS tooteid,
    ROUND(AVG(p.retail_price), 2) AS keskmine_hind,
    MIN(p.retail_price) AS min_hind,
    MAX(p.retail_price) AS max_hind
FROM products p
GROUP BY p.category
ORDER BY tooteid DESC, keskmine_hind DESC;


-- 2. Müüdud vs laos kategooriate lõikes
-- HAVING jätab alles ainult need kategooriad, kus on müüdud üle 3500 ühiku.
WITH myyk_toote_kohta AS (
    SELECT
        p.product_id,
        p.category,
        SUM(s.quantity) AS myydud_kogus,
        SUM(s.total_price) AS myygitulu
    FROM products p
    JOIN sales s
        ON s.product_id = p.product_id
    GROUP BY
        p.product_id,
        p.category
),
laoseis_toote_kohta AS (
    SELECT
        i.product_id,
        SUM(i.quantity_available) AS laos_kokku,
        SUM(i.reorder_point) AS tellimispiir_kokku
    FROM inventory i
    GROUP BY i.product_id
)
SELECT
    m.category,
    COUNT(*) AS aktiivseid_tooteid,
    SUM(m.myydud_kogus) AS myydud_kokku,
    COALESCE(SUM(l.laos_kokku), 0) AS laos_kokku,
    ROUND(
        SUM(m.myydud_kogus)::numeric / NULLIF(COALESCE(SUM(l.laos_kokku), 0), 0),
        2
    ) AS muydud_lao_suhe,
    ROUND(AVG(m.myydud_kogus), 2) AS keskmine_myydud_toote_kohta,
    ROUND(SUM(m.myygitulu), 2) AS myygitulu,
    SUM(
        CASE
            WHEN COALESCE(l.laos_kokku, 0) < COALESCE(l.tellimispiir_kokku, 0) THEN 1
            ELSE 0
        END
    ) AS alla_tellimispiiri_tooteid
FROM myyk_toote_kohta m
LEFT JOIN laoseis_toote_kohta l
    ON l.product_id = m.product_id
GROUP BY m.category
HAVING SUM(m.myydud_kogus) > 3500
ORDER BY muydud_lao_suhe DESC, myydud_kokku DESC;


-- 3. Toodete järjestus kategooria sees + TOP 3 ja müügi jaotus
WITH toodete_muuk AS (
    SELECT
        p.category,
        p.product_id,
        p.product_name,
        p.retail_price,
        SUM(s.quantity) AS myydud_kogus,
        SUM(s.total_price) AS myygitulu
    FROM products p
    JOIN sales s
        ON s.product_id = p.product_id
    GROUP BY
        p.category,
        p.product_id,
        p.product_name,
        p.retail_price
),
jarjestatud AS (
    SELECT
        category,
        product_id,
        product_name,
        retail_price,
        myydud_kogus,
        ROUND(myygitulu, 2) AS myygitulu,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY myydud_kogus DESC, retail_price DESC
        ) AS koht_kategoorias,
        ROUND(
            100.0 * myydud_kogus
            / SUM(myydud_kogus) OVER (PARTITION BY category),
            2
        ) AS osakaal_kategooria_myygist,
        ROUND(
            100.0 * myygitulu
            / SUM(myygitulu) OVER (PARTITION BY category),
            2
        ) AS osakaal_kategooria_kaibest
    FROM toodete_muuk
)
SELECT
    category,
    koht_kategoorias,
    product_id,
    product_name,
    retail_price,
    myydud_kogus,
    myygitulu,
    osakaal_kategooria_myygist,
    osakaal_kategooria_kaibest
FROM jarjestatud
WHERE koht_kategoorias <= 3
ORDER BY category, koht_kategoorias;


-- 4. Kokkuvõtlik kategooriaraport + soovitused
WITH muuk_kategoorias AS (
    SELECT
        p.category,
        SUM(s.quantity) AS myydud_kokku,
        ROUND(SUM(s.total_price), 2) AS myygitulu,
        ROUND(SUM((s.unit_price - p.cost_price) * s.quantity), 2) AS brutokasum
    FROM products p
    JOIN sales s
        ON s.product_id = p.product_id
    GROUP BY p.category
),
laoseis_kategoorias AS (
    SELECT
        p.category,
        SUM(i.quantity_available) AS laos_kokku,
        SUM(i.reorder_point) AS tellimispiir_kokku,
        COUNT(DISTINCT i.product_id) AS inventuuri_toodete_arv,
        COUNT(
            DISTINCT CASE
                WHEN i.quantity_available <= i.reorder_point THEN i.product_id
            END
        ) AS kriitilise_laoga_tooteid
    FROM products p
    LEFT JOIN inventory i
        ON i.product_id = p.product_id
    GROUP BY p.category
),
liikumised_kategoorias AS (
    SELECT
        p.category,
        SUM(
            CASE
                WHEN im.movement_type = 'IN' THEN ABS(im.quantity)
                ELSE 0
            END
        ) AS sisse_toodud_kogus,
        SUM(
            CASE
                WHEN im.movement_type = 'OUT' THEN ABS(im.quantity)
                ELSE 0
            END
        ) AS valja_liikunud_kogus,
        SUM(
            CASE
                WHEN im.movement_type = 'ADJUSTMENT' THEN ABS(im.quantity)
                ELSE 0
            END
        ) AS korrigeeritud_kogus
    FROM products p
    LEFT JOIN inventory_movements im
        ON im.product_id = p.product_id
    GROUP BY p.category
)
SELECT
    m.category,
    m.myydud_kokku,
    l.laos_kokku,
    ROUND(m.myydud_kokku::numeric / NULLIF(l.laos_kokku, 0), 2) AS muydud_lao_suhe,
    m.myygitulu,
    m.brutokasum,
    l.kriitilise_laoga_tooteid,
    lk.sisse_toodud_kogus,
    lk.valja_liikunud_kogus,
    lk.korrigeeritud_kogus,
    CASE
        WHEN ROUND(m.myydud_kokku::numeric / NULLIF(l.laos_kokku, 0), 2) >= 0.06
            THEN 'Kiire labiMyyk: hoia TOP-toodetel laoseis tugev ja planeeri sagedasem taistellimine.'
        WHEN m.brutokasum >= 250000
            THEN 'Kasumlik kategooria: hoia premium-tooted esilehel ja vaata, kas lao mahtu saab optimeerida.'
        WHEN l.kriitilise_laoga_tooteid > 0
            THEN 'Madal laoseis osadel toodetel: kontrolli replenishment reegleid ja poeladude jaotust.'
        ELSE 'Stabiilne kategooria: sobib bundle-pakkumisteks ja ristmyygiks.'
    END AS soovitus
FROM muuk_kategoorias m
JOIN laoseis_kategoorias l
    ON l.category = m.category
JOIN liikumised_kategoorias lk
    ON lk.category = m.category
ORDER BY m.brutokasum DESC, muydud_lao_suhe DESC;
