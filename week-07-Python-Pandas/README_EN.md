# Week 7: Python Pandas

Estonian version: [README.md](README.md)

This week I learned how to use Python and the pandas library for data analysis. In previous weeks, I worked a lot with SQL and dashboards, but now I understood how the same data can be explored, cleaned, joined, calculated, and visualized more flexibly in Python.

First, I learned what a pandas DataFrame is. I understood that a DataFrame is similar to an SQL table or an Excel worksheet, but in Python it can be used for more intermediate calculations and transformations. I practiced loading data and doing initial exploration with `read_csv()`, `head()`, `info()`, `describe()`, `shape`, and `dtypes`. These commands helped quickly understand how many rows and columns are in the dataset, what the data types are, and whether the data may contain problems.

Second, I learned to connect pandas logic with SQL. For example, SQL's `WHERE` condition corresponds to filtering with boolean indexing in pandas, `GROUP BY` corresponds to `groupby()`, and SQL `JOIN` corresponds to `merge()`. This helped me understand that I am not learning a completely new way of thinking from zero, but translating already familiar SQL logic into Python.

I also learned to filter and group data. For example, I could select only Tallinn orders, find larger purchases, calculate revenue by city, and compare customer purchase behavior. I understood that in pandas it is important to use the correct syntax, especially for filters with multiple conditions, where the `&` symbol must be used and conditions must be placed in parentheses.

Third, I learned to use the `merge()` function to join data. This was familiar from the SQL JOINs week, but in pandas the joining happens between DataFrames. I understood why `how="left"` is useful when I want to keep all sales rows and add customer information only when the matching `customer_id` exists in the customer table.

In addition, I learned to create new calculated columns. For example, a column can be added to mark order size, VIP status, or segment. This helped me see that Python is well suited for multi-step analysis where the result does not come from one query, but from gradually enriching the data.

An important part of this week was visualization with Plotly Express. I learned to create interactive bar charts, line charts, pie charts, and scatter plots. I understood that Plotly makes it possible to present Python analysis visually right away, and charts can be used both to check data and explain results.

The most important practical topic was RFM analysis. I learned that RFM means `Recency`, `Frequency`, and `Monetary`. Recency shows how recently a customer bought, Frequency shows the number of purchases, and Monetary shows the customer's total spending. Based on these three metrics, customers can be divided into segments such as `VIP Champions`, `Loyal Customers`, `Potential Loyalists`, `At Risk`, and `Lost`.

Through the UrbanStyle example, I understood why RFM analysis is useful for business. It does not only show how much sales happened, but helps understand which customers are the most valuable, who has potential to become loyal, and which customers may be lost. Based on this information, Marko can plan different campaigns for different customer groups.

In summary, this week I learned to:

- load data into a pandas DataFrame;
- explore dataset structure and quality;
- use `head()`, `info()`, `describe()`, `shape`, and `dtypes`;
- filter data with pandas boolean indexing;
- use `groupby()` to summarize data;
- sort results with `sort_values()`;
- join tables with `merge()`;
- create new calculated columns;
- connect pandas operations with SQL `WHERE`, `GROUP BY`, `JOIN`, and `ORDER BY` logic;
- create interactive charts with Plotly Express;
- understand the principle of RFM analysis;
- divide customers into segments based on purchase behavior;
- think about how data analysis supports marketing and business strategy.

This week I understood that Python and pandas give an analyst more flexibility than only SQL. SQL is very good for querying data, but Python helps process, clean, calculate, visualize, and turn data into a business conclusion. Through RFM analysis, I saw how sales rows can be turned into concrete customer segments that support better decisions.
