# Run the dashboard on localhost

## Windows (PowerShell)
Install Python 3.10+ and Git, then:

```powershell
git clone https://github.com/chaima-menouar/ga4-ecommerce-marketing-analytics.git
cd ga4-ecommerce-marketing-analytics
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open http://localhost:8501 if your browser does not open automatically.

## macOS / Linux
```bash
git clone https://github.com/chaima-menouar/ga4-ecommerce-marketing-analytics.git
cd ga4-ecommerce-marketing-analytics
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Display real data
Run the four SQL files under `sql/` in BigQuery and download each result as CSV.
Upload the corresponding CSV files in the app tabs. Do not upload personal or confidential data.

This local Streamlit dashboard is a supplementary prototype; the course's Looker Studio deliverable still needs to be created and shared separately.
