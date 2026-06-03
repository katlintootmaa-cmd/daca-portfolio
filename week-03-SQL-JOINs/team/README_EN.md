# Week 3: Team Work

Estonian version: [README.md](README.md)

## What We Did

During this week's team work, we applied SQL JOINs to solve UrbanStyle's business problem. The goal was to help Anna and Toomas get answers to questions that require combining several tables: who buys, who does not buy, which products sell, which products do not sell, and which sales channels work best.

## Team Work Focus

We worked with the `sales`, `customers`, `products`, and, when needed, inventory data tables. We used the JOIN types learned in the session to create practical queries and interpret results in a business context.

## Roles and Tasks

- Role A: Mari was responsible for connecting sales and customers with `INNER JOIN`.
- Role B: Kätlin found customers who registered but had not purchased, using the `LEFT JOIN + WHERE IS NULL` pattern.
- Role C: Ragnar analyzed products and inventory with `LEFT JOIN` logic to find unsold or risky products.
- Role D: Karmo compared marketing and sales relationships with `INNER JOIN` and interpreted the impact of channels.
- Connecting sales and customers with `INNER JOIN` to find purchasing customers and top customers by total sales.
- Finding customers who registered but never purchased, using the `LEFT JOIN + WHERE IS NULL` pattern.
- Finding unsold products with `LEFT JOIN` and analyzing inventory data.
- Comparing sales channels to understand which channels bring the most sales and customers.
- Combining several tables to see customer, sales, and product information together.
- Analyzing missing relationships, or using anti-JOIN logic, for customers and products.

## Role Descriptions

- Role A, the sales and customer connector, was responsible for the view of customers who had purchased. The goal was to show which customers create sales and how `INNER JOIN` helps create a customer-based sales picture.
- Role B, the analyst of customers without purchases, was responsible for finding missing purchase relationships. The role used `LEFT JOIN` and `WHERE IS NULL` logic to identify customers who have an account but no purchase history.
- Role C, the product and inventory analyst, was responsible for identifying unsold or risky products. The role connected product and inventory data to evaluate where inventory or sales potential problems appear.
- Role D, the marketing and sales connector, was responsible for channel impact analysis. The role connected marketing or sales channel information with sales results and interpreted which channels create business value.

## Work Process

- We read Anna and Toomas's challenge.
- We divided roles and subtasks between team members.
- Each participant wrote SQL queries based on their role.
- We checked whether the queries worked and whether the JOIN conditions were correct.
- We shared results in the team and interpreted them in a way Anna could understand.
- We summarized the main findings, surprises, recommendations, and missing data into one shared output.

## SQL Skills Used

- `INNER JOIN`
- `LEFT JOIN`
- `LEFT JOIN + WHERE IS NULL`
- joining multiple tables
- `GROUP BY`
- `ORDER BY`
- `COUNT`
- `SUM`
- table aliases
- translating a business question into an SQL query

## Main Lessons Learned

- JOINs help connect data from different tables into one complete picture.
- `INNER JOIN` is suitable when we want to see only existing matches, such as customers who have purchased.
- `LEFT JOIN + WHERE IS NULL` is suitable for finding missing relationships, such as customers without purchases or unsold products.
- Multi-table JOINs help answer more complex business questions, such as which product categories sell best in which channels or cities.
- An SQL query result alone is not enough; it is also important to add business interpretation and a recommendation.

## Summary

As a result of the team work, we practiced using SQL JOINs to solve a real UrbanStyle business problem. We learned to divide the analysis into smaller role-based tasks, write JOIN queries, and summarize the results into an understandable recommendation for Anna. This work prepares for next week's topic, where JOINs are combined with summary calculations, `GROUP BY`, `HAVING`, CTEs, and window functions.
