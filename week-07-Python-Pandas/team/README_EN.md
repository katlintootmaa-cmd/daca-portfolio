# Week 7 Team Work: RFM Customer Segmentation

Estonian version: [README.md](README.md)

## Files

- `week7_rfm_complete.ipynb` - complete group work notebook with roles A, B, C, and D.
- `rfm_segments.csv` - customer segments exported from Supabase data for the marketing team.
- `rfm_segmentide_jaotus.png`, `rfm_segmentide_scatter.png`, `rfm_top_10_vip.png` - RFM result visuals.

## Data Source

The notebook uses a Supabase connection from the `.env` file:

```python
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
```

The required packages are available in the project's `.venv` environment. When opening the notebook, choose the project virtual environment as the kernel.

## Roles

- Role A: Mari loads the `sales` and `customers` tables from Supabase and merges them by `customer_id`.
- Role B: Kätlin cleans the data, removes duplicates, NULLs, invalid dates, and non-positive amounts.
- Role C: Ragnar calculates Recency, Frequency, and Monetary values and assigns RFM segments.
- Role D: Karmo creates three Plotly charts and writes recommendations for Marko.

## Role Descriptions

- Role A, the data loader, was responsible for getting the required tables from Supabase and joining them. The output was a joined dataset ready for analysis, where sales and customer information are connected.
- Role B, the data cleaner, was responsible for the pandas cleaning steps. The role removed duplicates, invalid dates, empty values, and illogical amounts so that the RFM result would be reliable.
- Role C, the RFM analyst, was responsible for Recency, Frequency, and Monetary calculations. The role assigned scores and segments and checked that the segment logic matched the marketing goal.
- Role D, the visualizer and recommendation writer, was responsible for presenting the results. The role created charts, interpreted segments, and wrote campaign recommendations for Marko.

## Date Limit

The analysis uses `2025-02-28` as the RFM reference date and filters all later sales rows out of the RFM input. This means the Week 7 work uses data up to the end of February 2025.

## Analytical Interpretation

Week 7 is the foundation layer of the RFM analysis: it shows which customers bought recently, bought often, and brought the most revenue. The business meaning of the segments is:

- `VIP Champions`: keep these customers with personal communication, early access offers, and special loyalty program treatment.
- `Loyal`: increase average basket size with cross-sell and bundle offers.
- `Potential`: guide them toward the second and third purchase so they move into a more loyal segment.
- `At Risk`: launch a win-back campaign before customers move into the lost segment.
- `Lost`: test low-cost reactivation and keep campaign ROI under control.

## Recommended Next Steps

- Add a concrete campaign goal, channel, offer, and metric to each segment.
- Compare segments by city, channel, and product category.
- Measure campaigns with a control group, not only with a before/after comparison.
- Continue the same logic in the Week 8 pipeline with an automated report, cohort retention, and A/B test plan.
