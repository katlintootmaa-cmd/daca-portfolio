# Week 8: What I Learned

Estonian version: [README.md](README.md)

During this week, I learned how to turn the previous RFM analysis into an automated Python pipeline. Earlier I worked more with CSV files, but now I could request data directly through the Supabase API. I understood why using an API is practical: the report can take fresh data directly from the source and I do not need to export files manually.

I also learned that API queries need a proper structure. Supabase returns a limited number of rows with one query, so I added paginated data loading. This helped fetch the full sales and customer dataset, not only the first rows.

While building the pipeline, I understood ETL logic better:

- Extract: I fetch data through the API or use sample data if needed.
- Transform: I clean the data, join tables, and calculate reports.
- Validate: I check that the data and totals are logical.
- Load: I save the results as CSV and HTML reports.

An important learning point for me was also that API keys must not be written directly into Python code. I kept the Supabase URL and key in the `.env` file and understood why `.gitignore` is needed to protect sensitive information.

In the RFM analysis, I repeated the Recency, Frequency, and Monetary principle, but this time I automated it. This means the same logic can be used again each time the data updates.

On the visualization side, I learned to use Plotly charts and save results as HTML files. This makes pipeline outputs easier to open, share, and compare.

In summary, I understood how Python, pandas, the Supabase API, logging, validation, and visualization work together as one repeatable data pipeline. This week showed me how manual analysis can become a tool that can be run again and later automated.

## File Structure

- `individual/` - my individual work files, pipeline demo, and visual exports.
- `team/` - team work modular pipeline.
- `individual/week8_individual_summary.md` - more detailed description of individual work.
- `individual/Python API ja automatiseeritud RFM pipeline.md` - more detailed explanation of the API pipeline.
