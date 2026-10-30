# Looker Studio dashboard specification

Connect BigQuery results through saved tables/views in your Google Cloud project.

Pages:
1. Executive summary — sessions, purchases, purchase revenue, session purchase rate, date filter.
2. Acquisition — first-user source/medium, sessions and purchases; label attribution caveat.
3. Funnel — sessions containing view_item, add_to_cart, begin_checkout and purchase (non-sequential).
4. Recommendations — insights derived **only after running queries**.

Data sources: outputs of `sql/01_daily_sessions.sql` through `sql/04_funnel.sql`.
Never use illustrative figures as actual results. Dashboard URL: **not published yet**.
