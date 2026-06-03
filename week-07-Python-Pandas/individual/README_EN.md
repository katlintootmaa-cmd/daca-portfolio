# Week 7: Python Pandas - RFM Customer Segmentation

Estonian version: [README.md](README.md)

## My Role

Role B: Data Cleaning. My task was to take the sales and customer DataFrame merged by Role A, remove duplicates, handle critical NULL values, parse dates, and remove invalid or non-positive `total_price` values.

## Main Findings

- During cleaning, the most important thing is to protect the input for RFM analysis: `customer_id`, `sale_date`, and `total_price` must not be empty because Recency, Frequency, and Monetary values are calculated from them.
- Based on Supabase data, 8,950 sales rows and 2,540 unique customers remained after cleaning.
- The VIP Champions segment contributes the largest share of revenue, even though it is not the largest customer group.

## AI Usage

I used AI to interpret the instructions, build the Role B cleaning flow, and convert the team notebook to use Supabase. AI helped add checks, reports, and exports so that the notebook follows the group work instructions.

## Files

- `individual/week7_rfm_B.ipynb` - my individual Role B notebook.
- `team/week7_rfm_complete.ipynb` - complete team notebook with roles A, B, C, and D.
- `team/rfm_segments.csv` - exported customer segments.
