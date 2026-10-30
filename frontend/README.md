# NEXUS — React dashboard

Premium responsive React/Vite frontend with Recharts, Lucide icons, and browser-local BigQuery CSV import.

## Run locally

Requires Node.js 18+.

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

## Data

Showcase mode starts **ON** and uses clearly labeled synthetic figures for design preview. Toggle it OFF to see empty states. On **Data sources**, upload the CSV exports of `sql/01_daily_sessions.sql`, `02_purchases.sql`, `03_channels.sql`, and `04_funnel.sql`. Files stay in your browser memory; no backend receives them.

```bash
npm run build
npm run preview
```

## Important

React is the polished frontend. The existing Python Streamlit app and BigQuery client remain in the repository as an optional analysis backend. The university also requires a separate Looker Studio report, which has not been published. This React app does not itself connect directly to BigQuery, and does not display real numbers until CSVs are provided.
