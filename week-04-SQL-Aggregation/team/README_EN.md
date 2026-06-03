# Week 4: Team Work

Estonian version: [README.md](README.md)

## Role Distribution

| Role | Team Member | Task |
|------|-------------|------|
| A | Karmo | Sales summary data: calculated sales KPIs, period comparisons, and main revenue patterns. |
| B | Mari | Customer group analysis: summarized customers by segments, cities, or purchase behavior. |
| C | Kätlin | Inventory statistics: analyzed stock levels, product availability, and inventory risks. |
| D | Ragnar | Marketing campaign ROI: evaluated the impact of campaigns on sales and customer activity. |

## Role Descriptions

- Role A, the sales summary analyst, was responsible for management-level sales KPIs. The role calculated revenue, number of orders, average purchase, and period comparisons.
- Role B, the customer group analyst, was responsible for the customer summary view. The role found customer segments, more active customers, and groups that marketing or sales should pay attention to.
- Role C, the inventory statistics analyst, was responsible for the overall view of stock levels and product inventory. The role evaluated which categories or products need more attention in inventory management.
- Role D, the marketing ROI analyst, was responsible for measuring campaign performance. The role compared the impact of campaigns on sales, customer activity, and channel profitability.

## What We Did

During this week's team work, we applied SQL aggregation to solve UrbanStyle's business problem. The goal was to prepare summary reports for Kristi's board meeting, giving a quick overview of sales, customer groups, inventory, and marketing performance.

## Team Work Focus

We worked with the `sales`, `customers`, `products`, `inventory`, and, where possible, `web_logs` tables. We used techniques learned in the session, such as `GROUP BY`, `HAVING`, CTEs, and window functions, to turn raw data into business-readable summaries.

## Roles and Tasks

- Role A: sales summary data by months and categories to find revenue trends, order counts, and average order value.
- Role B: customer group analysis to segment customers into `VIP`, `Regular`, and `New` groups and find top customers.
- Role C: inventory statistics to compare stock levels, sales, and gross profit by categories and products.
- Role D: marketing campaign ROI to evaluate channel and source performance and identify measurement gaps.

## Work Process

- We read Anna Mets's challenge and defined what summary numbers Kristi needs for the board.
- We divided roles in the team by domains.
- Each participant wrote SQL queries and a short business summary based on their subtask.
- We checked that the queries used at least `GROUP BY`, and where needed `HAVING`, CTEs, or window functions in more complex solutions.
- We presented our findings to each other and summarized the main conclusions into a shared output.

## SQL Skills Used

- `GROUP BY`
- `HAVING`
- `COUNT`
- `SUM`
- `AVG`
- `MIN` and `MAX`
- `CASE WHEN`
- CTE, or `WITH`
- `LAG()` and other window functions
- joining tables with `JOIN`

## Main Lessons Learned

- Aggregation helps turn many individual rows into key metrics that management can understand.
- `HAVING` is needed when we want to filter already summarized groups, not individual rows.
- CTEs make more complex queries easier to read and help divide analysis into steps.
- Business value appears when interpretation and recommendation are added to the numbers.
- Marketing analysis depends strongly on data quality; if all channels are not measured correctly, part of the picture remains incomplete.

## Summary

As a result of the team work, we created a summary view for UrbanStyle that connects sales trends, customer segments, inventory, and marketing impact into one business logic. We learned how `GROUP BY`, `HAVING`, CTEs, and window functions help answer CEO-level questions and how the results of different roles can be combined into one clear report.
