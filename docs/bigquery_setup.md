# BigQuery live connection — local Windows

1. Install the Google Cloud CLI and sign in with an account authorized for a Google Cloud project.
2. Run `gcloud auth application-default login` in PowerShell.
3. Set the quota/billing project if needed: `gcloud auth application-default set-quota-project YOUR_PROJECT_ID`.
4. In your cloned repository run `python -m pip install -r requirements.txt` and `python -m streamlit run app.py`.
5. In the sidebar select **BigQuery (live)**, enter the Google Cloud project ID, and press **Load real GA4 data**.

Queries are read-only and have a maximum-bytes-billed guard. Check project billing, quotas, permissions and expected costs. Never commit OAuth tokens or service-account JSON. The public sample is historical and obfuscated.

For Looker Studio, connect your own saved query result tables or views, then build charts following `dashboard/README.md`. A localhost Streamlit app is not a substitute for a published Looker Studio report.
