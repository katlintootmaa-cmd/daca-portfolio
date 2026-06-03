# Week 2: SQL Cleaning

Estonian version: [README.md](README.md)

# Summary: What I Learned

This week I learned data cleaning in SQL and understood that before doing analysis, data quality must always be checked. I learned that incorrect or messy data can lead to completely wrong conclusions, so data should not be changed immediately. First, problems need to be identified, documented, tested, and only then fixed.

First, I learned how to find duplicates. I understood how to use `GROUP BY` and the `HAVING` condition to find values that appear more than once. I also learned to use the `ROW_NUMBER()` function to number rows within the same group and separate the original record from duplicates. This helped me understand how to decide which row to keep and which one is an extra copy.

Second, I learned to understand `NULL` values better. I learned that `NULL`, an empty string (`''`), and the number `0` do not mean the same thing in SQL. I learned to use `IS NULL` and `IS NOT NULL` to find missing data, and the `COALESCE()` function to display a clear default value instead of missing values. I also understood that `NULL` values must not be checked with `= NULL`, because that does not work correctly.

Third, I learned to standardize data formats. I practiced cleaning text with functions such as `TRIM()`, `UPPER()`, `LOWER()`, and `INITCAP()` to remove extra spaces and make spelling consistent. I also learned date formatting and conversion using date functions, `TO_CHAR()`, and `CAST()`. This helped me understand why values with the same meaning can appear in different forms in a database and why they must be standardized before analysis.

I also understood that data cleaning is not only writing SQL queries, but also checking data quality across different tables. Based on the group work guide, I learned to look at data by domains: sales data, customer data, product data, and cross-validation between tables. This taught me to check whether a sale refers to an existing customer and product, and whether prices and quantities match logically.

An important lesson was also a safe way of working. I learned that data cleaning should be done on a test copy, not in the production table. Before making changes, the problems must be counted, described in a report, and only then corrected. This helped me understand that a data analyst's work is not only getting a result, but also following a correct and reliable process.

One thing I remembered clearly from the documents was how much impact faulty data can have. For example, the sales table contained thousands of duplicates, missing `customer_id` values, and even future dates. This showed me practically how low-quality data can distort sales reports and lead to wrong business decisions.

In summary, this week I learned to:

- find duplicates with `GROUP BY`, `HAVING`, and `ROW_NUMBER()`;
- identify and handle missing values with `IS NULL`, `IS NOT NULL`, `COALESCE()`, and `NULLIF()`;
- clean and standardize text fields and dates;
- work safely with a test copy before changing real data;
- create a cleaning report where the SQL result is also translated into business meaning.

This week I understood that clean data is the foundation of reliable analysis. If data is not checked and cleaned, the quality of reports and decisions cannot be trusted.
