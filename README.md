# E-Commerce Marketing Performance Analytics
GA4 × BigQuery × Looker Studio — TDIA3, Webmarketing et CRM (2026–2027).

## Objective
Measure sessions, purchases, channel performance and the e-commerce funnel using the public, obfuscated Google Merchandise Store GA4 export.

**Dataset:** `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` (2020-11-01 to 2021-01-31).

## Deliverables
- `sql/`: BigQuery Standard SQL queries.
- `docs/tracking_plan.md`: GA4 tagging, consent and missing-data limitations.
- `dashboard/README.md`: Looker Studio setup and suggested charts.
- `presentation/outline.md`: 12-minute demonstration plan.

## Run
1. Open BigQuery in a Google Cloud project with billing/permissions configured.
2. Execute the SQL files in order; check query costs before running.
3. Export results or create views in your own project to connect Looker Studio.
4. Record actual results and share the dashboard link; **no KPI has been verified yet**.

This repository contains reproducible analysis code, not a published dashboard or executed results. Public sample data is historical and obfuscated.
