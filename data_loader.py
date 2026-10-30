"""Read GA4 BigQuery public sample with Application Default Credentials."""
from pathlib import Path
from google.cloud import bigquery

SQL_FILES = {
    "daily": "01_daily_sessions.sql",
    "purchases": "02_purchases.sql",
    "channels": "03_channels.sql",
    "funnel": "04_funnel.sql",
}

def fetch_all(project_id: str, maximum_bytes_billed: int = 2_000_000_000):
    """Execute four read-only queries, returning pandas DataFrames.

    Authentication is supplied by Google Application Default Credentials.
    A billing-enabled GCP project may be required. This function does not
    create datasets, modify tables, or write credentials to disk.
    """
    if not project_id or not project_id.strip():
        raise ValueError("A Google Cloud project ID is required.")
    client = bigquery.Client(project=project_id.strip())
    root = Path(__file__).resolve().parent / "sql"
    results = {}
    for key, filename in SQL_FILES.items():
        sql = (root / filename).read_text(encoding="utf-8")
        job_config = bigquery.QueryJobConfig(
            maximum_bytes_billed=maximum_bytes_billed,
            use_query_cache=True,
        )
        results[key] = client.query(sql, job_config=job_config).result().to_dataframe()
    return results
