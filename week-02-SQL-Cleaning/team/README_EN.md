# Week 2 Team Work: SQL Cleaning

Eestikeelne versioon: [README.md](README.md)

## Summary

Week 2 focused on data quality. The team searched for duplicates, missing values, invalid dates, illogical amounts, and inconsistencies between tables so that before analysis it would be clear how reliable UrbanStyle's data is.

## Role Distribution

| Role | Team Member | Task |
|------|-------------|------|
| A | Kätlin | Sales data cleaning: checked duplicates, dates, amounts, and empty customer relationships in the `sales` table. |
| B | Ragnar | Customer data cleaning: checked missing values, email/city fields, and duplicate records in the `customers` table. |
| C | Karmo | Product data cleaning: checked categories, prices, and product code consistency in the `products` table. |
| D | Mari | Cross-validation and quality control: compared relationships between tables and summarized quality risks. |

## Role Descriptions

- Role A, the sales data cleaner, was responsible for making sure that sales row amounts, dates, and customer relationships were usable for analysis. The focus was on finding incorrect or incomplete sales records.
- Role B, the customer data cleaner, was responsible for the consistency of customer information. The role checked empty fields, duplicate customers, and whether contact or location information was suitable for later segmentation.
- Role C, the product data cleaner, was responsible for the quality of the product catalog. The role checked prices, categories, and product identifiers so that product analysis would not produce misleading results.
- Role D, the quality control coordinator, reviewed data across tables. The role's task was to find relationship issues, such as sales without a customer or product, and summarize the risks in a shared overview.

## Main Skills

- Using `IS NULL`, `DISTINCT`, `COUNT`, `GROUP BY`, and conditional filters in quality control.
- Finding problematic records before analysis.
- Explaining the impact of data quality in business language.

## Output

The team created a data cleaning overview that describes the main quality problems and provides a foundation for the following week's JOIN analysis.
