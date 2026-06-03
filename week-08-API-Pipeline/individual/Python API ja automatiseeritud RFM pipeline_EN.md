# Python API and Automated RFM Pipeline

This work explains how an RFM analysis can be turned into a more automated Python pipeline.

## Main Idea

Instead of using only local CSV files, the pipeline can get fresh data from Supabase through an API. This makes the analysis easier to repeat and update.

## Pipeline Steps

- Extract: get data from the API or fallback data.
- Transform: clean and combine the data.
- Analyze: calculate KPIs and RFM segments.
- Validate: check that the results make sense.
- Load: save charts and reports as files.

## What I Learned

I learned that automation is useful when the same analysis has to be repeated. I also learned that API keys should be stored in a `.env` file and not written directly into the code.

## Summary

This task helped me understand how Python, pandas, API requests, validation, and reporting can work together in one repeatable workflow.
