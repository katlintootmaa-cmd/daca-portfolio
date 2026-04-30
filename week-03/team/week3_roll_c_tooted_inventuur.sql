-- Week 3, Roll C: tooted + inventuur
-- Eesmärk: leida müümata tooted, enim müüdud tooted,
-- kategooriate tulemused ja laoseisu täiendamise vajadus.

-- 1. Tooted, mida pole kunagi müüdud
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.subcategory,
    p.retail_price,
    s.sale_id
FROM products p
LEFT JOIN sales s
    ON p.product_id = s.product_id
WHERE s.sale_id IS NULL
ORDER BY p.product_id;

-- 2. Mitu müümata toodet on?
SELECT
    COUNT(*) AS myymata_tooteid
FROM products p
LEFT JOIN sales s
    ON p.product_id = s.product_id
WHERE s.sale_id IS NULL;

-- 3. Enim müüdud tooted kogumüügi järgi
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.subcategory,
    COUNT(s.sale_id) AS myydud_kordi,
    SUM(s.quantity) AS myydud_yhikuid,
    ROUND(SUM(s.total_price), 2) AS kogumyyk
FROM products p
INNER JOIN sales s
    ON p.product_id = s.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.subcategory
ORDER BY kogumyyk DESC
LIMIT 10;

-- 4. Kategooriate müük
SELECT
    p.category,
    COUNT(DISTINCT p.product_id) AS tooteid,
    COUNT(s.sale_id) AS myyke,
    COALESCE(ROUND(SUM(s.total_price), 2), 0) AS kogumyyk,
    COALESCE(ROUND(AVG(s.total_price), 2), 0) AS keskmine_ost
FROM products p
LEFT JOIN sales s
    ON p.product_id = s.product_id
GROUP BY p.category
ORDER BY kogumyyk DESC;

-- 5. Inventuuri staatus asukohtade kaupa
SELECT
    p.product_id,
    p.product_name,
    p.category,
    i.location,
    i.quantity_available,
    i.reorder_point,
    CASE
        WHEN i.inventory_id IS NULL THEN 'PUUDUB INVENTUURIST'
        WHEN i.quantity_available <= i.reorder_point THEN 'TELLI JUURDE'
        ELSE 'OK'
    END AS staatus
FROM products p
LEFT JOIN inventory i
    ON p.product_id = i.product_id
ORDER BY
    staatus DESC,
    i.quantity_available ASC NULLS FIRST,
    p.product_id;

-- 6. Kui palju laoridu vajab täiendamist?
SELECT
    i.location,
    COUNT(*) AS telli_juurde_ridu
FROM inventory i
WHERE i.quantity_available <= i.reorder_point
GROUP BY i.location
ORDER BY telli_juurde_ridu DESC;

-- 7. Edasijõudnute tase: tooted, mis on laos, aga pole kunagi müüdud
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.retail_price,
    i.location,
    i.quantity_available,
    ROUND(p.retail_price * i.quantity_available, 2) AS kinni_olev_raha
FROM products p
LEFT JOIN sales s
    ON p.product_id = s.product_id
LEFT JOIN inventory i
    ON p.product_id = i.product_id
WHERE s.sale_id IS NULL
  AND i.quantity_available > 0
ORDER BY kinni_olev_raha DESC;

-- 8. Müümata tooted, millel puudub inventuurikirje
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.subcategory,
    p.retail_price,
    COUNT(i.inventory_id) AS inventuuri_ridu
FROM products p
LEFT JOIN sales s
    ON p.product_id = s.product_id
LEFT JOIN inventory i
    ON p.product_id = i.product_id
WHERE s.sale_id IS NULL
GROUP BY
    p.product_id,
    p.product_name,
    p.category,
    p.subcategory,
    p.retail_price
HAVING COUNT(i.inventory_id) = 0
ORDER BY p.product_id;

-- Kokkuvõte Annale ja Toomasele:
-- Andmetes on 362 toodet, millest 350 on vähemalt korra müüdud ja 12 pole kordagi müüdud.
-- Kõige edukam toode on "Õhuline sünteetiline sporditossud": 35 müügirida ja 27347.04 eurot kogumüüki.
-- Kategooriatest juhib "jalanõusid" 774034.75 euroga; sellele järgnevad "meeste_riided" ja "naiste_riided".
-- Inventuuris on 231 laorida, kus quantity_available on reorder_point tasemel või sellest madalam.
-- Müümata 12 toodet ei ole inventory tabelis laoseisuga seotud, seega tuleks kontrollida,
-- kas need on päriselt aktiivsed tooted või kataloogi jäänud vanad/mitteaktiivsed kirjed.
