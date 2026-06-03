# Week 10 Team Work: Portfolio Defense

Eestikeelne versioon: [README.md](README.md)

## Goal

The goal of the Week 10 team task was to prepare a 7-minute portfolio defense in the format of an UrbanStyle board meeting. The presentation needed to answer one key question:

> What did UrbanStyle actually learn from our data work, and which decision could change because of it?

The focus was impact, not a list of completed files. We combined 10 weeks of work into one business story: data problems, main findings, strongest visuals, board-level recommendations, and an honest reflection on AI use.

## Team Mission

Our mission was to help UrbanStyle move from intuition-based decisions toward more data-driven management. We used SQL, Power BI, Python/Pandas, an API pipeline, and GitHub documentation to turn sales, customer, and reporting data into decision-ready insights.

## Roles

| Role | Team member | Responsibility |
|------|-------------|----------------|
| Portfolio quality control | Kätlin | README structure, business explanation, evidence, and defense logic |
| Deploy and link checks | Ragnar | Public access, broken links, file opening, and technical usability |
| Technical review | Karmo | SQL/Python files, notebooks, pipelines, and reproducibility |
| Presentation and business message | Mari | Value proposition, board recommendations, transitions, and data storytelling |

My role was portfolio quality control. I checked that the work would be understandable to someone who does not know the course background: each important project needed a problem, approach, result, lesson learned, and AI usage explanation.

## 7-Minute Presentation Plan

| Part | Time | Speaker | Content |
|------|------|---------|---------|
| Introduction | 1:00 | Mari | Team, mission, and UrbanStyle context |
| Data overview | 2:00 | Karmo | 3-5 key numeric findings and the biggest surprise |
| Visuals | 2:00 | Kätlin | Power BI dashboards, RFM outputs, and API/Plotly examples |
| Board recommendations | 1:00 | Mari | 3 concrete data-based recommendations |
| AI use | 1:00 | Ragnar | How AI helped and where we had to decide ourselves |

## Key Findings for the Presentation

| Finding | Evidence | Why it matters to the board |
|---------|----------|-----------------------------|
| Revenue in 2024 grew by 19.08% compared with 2023. | [Power BI investor view](../../week-05-Visualization-Design/individual/README.md) | UrbanStyle has a growth story, but management needs to monitor which channels and categories drive that growth. |
| After cleaning, the RFM dataset contained 8,950 sales rows and 2,540 unique customers. | [RFM data cleaning in Python](../../week-07-Python-Pandas/individual/README.md) | Customer segmentation is based on a controlled and sufficiently large dataset. |
| The VIP Champions segment contributes a large share of revenue, even though it is not the largest customer group. | [RFM team output](../../week-07-Python-Pandas/team/README.md) | Marketing and loyalty work should focus on the most valuable customers, not only the largest segment. |
| Tallinn is UrbanStyle's main physical store and can be used as a benchmark for other locations. | [Tallinn store dashboard](../../week-06-Visualization-Storytelling/individual/README.md) | Management can use Tallinn's successful patterns to improve other locations. |
| The API pipeline made recurring report outputs reusable. | [API pipeline](../../week-08-API-Pipeline/individual/README.md) | Automation reduces manual work and keeps reporting quality more consistent. |

## Visuals to Show

1. [UrbanStyle investor dashboard](../../week-05-Visualization-Design/individual/week%205%20D.png) - shows growth, KPIs, and the investor-level overview.
2. [Tallinn store dashboard](../../week-06-Visualization-Storytelling/individual/week%206_A_K%C3%A4tlin.png) - shows a location-based data story and management view.
3. [RFM segment scatter plot](../../week-07-Python-Pandas/team/rfm_segmentide_scatter.png) - shows the difference between customer segments and the value of VIP customers.
4. [API pipeline HTML output](../../week-08-API-Pipeline/individual/combined_visuals.html) - shows that the analysis output can be automated and shared.

## 3 Recommendations for UrbanStyle's Board

1. Use Power BI dashboards in the weekly management rhythm, because 19.08% annual revenue growth needs regular monitoring by channel, category, and store.
2. Aim loyalty and marketing activities at the most valuable RFM segments, because VIP Champions contribute a large share of revenue even though they are not the largest customer group.
3. Automate recurring reports with the Python/API pipeline to reduce manual work, keep outputs consistent, and make data checks reusable.

## Short Presentation Script

**Introduction:**
Hello, we are UrbanStyle's data team. Our mission was to make sales, customer, and reporting data usable for management decisions over 10 weeks. We did not focus only on queries and dashboards, but on what UrbanStyle can decide based on them.

**Data overview:**
Our strongest growth number was that 2024 revenue increased by 19.08% compared with 2023. For the RFM analysis, we cleaned the data so that 8,950 sales rows and 2,540 unique customers remained. The biggest business surprise was that the VIP Champions segment contributes a large share of revenue, even though it is not the largest customer group.

**Visuals:**
The investor view shows growth and main KPIs on one screen. The Tallinn store dashboard shows how one strong physical store can be used as a benchmark for other locations. RFM visuals help identify which customers deserve special attention. The API pipeline output shows that the same reporting steps can be repeated without manually rebuilding the report every time.

**Recommendations:**
Our recommendation to the board is to use dashboards regularly, not only at the end of a project. Second, loyalty and marketing work should be connected to RFM segments. Third, recurring reports should be automated, because this saves time and reduces the risk of manual errors.

**AI use:**
AI helped with SQL and Python debugging, making README texts clearer, checking the presentation structure, and thinking through possible defense questions. We still checked the numbers, business conclusions, and final recommendations ourselves, because AI does not replace UrbanStyle context or analyst responsibility.

## Timing Check

| Part | Target time | Check |
|------|-------------|-------|
| Introduction | 1:00 | Fits if the mission is one sentence and member introductions are short |
| Data overview | 2:00 | Each finding is one sentence plus one number |
| Visuals | 2:00 | Show 2-3 visuals, not every file |
| Recommendations | 1:00 | Exactly 3 recommendations |
| AI use | 1:00 | 2-3 concrete examples plus one lesson |
| Total | 7:00 | Yellow signal at 6:00, finish the sentence at 7:00 |

## Quality Checklist

- The presentation follows the 5-part structure.
- The presentation fits within 7 minutes.
- At least 3 numeric findings are ready.
- At least 1 strong visual or dashboard opens quickly.
- 3 board recommendations are concrete and data-based.
- The AI usage reflection is honest and specific.
- Each team member knows their part and transitions are agreed.
- GitHub links, README files, Power BI screenshots, and HTML outputs open correctly.

## What We Learned

The main lesson from the team task was that a portfolio defense must communicate impact, not process. The board does not need a long list of every query and file. The board needs an answer to the question: what did the data show, and what should UrbanStyle do based on it?

We also learned that a good portfolio is evidence of collaboration. Technical work, visuals, business recommendations, and clear documentation need to form a story that can be understood and checked quickly.
