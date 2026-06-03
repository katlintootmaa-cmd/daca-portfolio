# Week 1: SQL Basics

Eestikeelne versioon: [README.md](README.md)

This week I learned the basic SQL commands and practiced reading, filtering, and counting data using the UrbanStyle database. The focus was on understanding how to explore data with queries without changing the original data.

## What I Learned

- with `SELECT` and `FROM`, I learned how to choose the needed columns and define which table to get data from
- with `ORDER BY` and `LIMIT`, I learned how to sort and limit query results
- with the `WHERE` clause, I learned how to filter data by different conditions
- I used comparison operators such as `=`, `>`, `<`, `>=`, `<=`
- I learned how to use logical operators `AND` and `OR`
- I understood how `BETWEEN`, `IN`, `LIKE`, and `IS NULL` work
- with `DISTINCT`, I learned how to find unique values
- with `COUNT(*)`, `COUNT(column)`, and `COUNT(DISTINCT column)`, I learned how to count rows and unique values

## What I Practiced

- reviewed the contents of the `sales`, `customers`, and `products` tables
- found the largest and smallest sales
- filtered data by date, amount, and channel
- searched for rows where `customer_id` was missing
- checked whether the tables contained duplicates
- compared the total number of rows with the number of unique `sale_id` values
- practiced noticing data quality issues, such as `NULL` values and possible duplicates

## Main Insights

- `SELECT *` is not a good practice when the goal is to work clearly and efficiently
- `NULL` is not the same as `0` or an empty value, so `IS NULL` must be used to find it
- `COUNT(*)` and `COUNT(column)` can return different results when the data contains missing values
- SQL helps find patterns and data issues quickly when the question is written clearly

## Summary

Week 1 gave me a strong foundation for using SQL. I learned how to write simple but practical queries for exploring, filtering, and checking data. Next, I want to become more confident in writing more complex queries and learn how to document my SQL work better.
