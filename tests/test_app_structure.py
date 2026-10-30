from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[1]

def test_python_syntax():
    for file in ("app.py", "data_loader.py"):
        ast.parse((ROOT / file).read_text(encoding="utf-8"))

def test_required_sql():
    for file in ("01_daily_sessions.sql", "02_purchases.sql", "03_channels.sql", "04_funnel.sql"):
        sql = (ROOT / "sql" / file).read_text(encoding="utf-8")
        assert "bigquery-public-data.ga4_obfuscated_sample_ecommerce" in sql
        assert "_TABLE_SUFFIX" in sql

def test_no_credentials_committed():
    assert not (ROOT / "service-account.json").exists()
