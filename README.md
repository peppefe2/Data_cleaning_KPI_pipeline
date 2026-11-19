# Order Cleaning & KPI Pipeline

Reproducible pipeline to clean messy order exports, log rejected rows, load SQLite, and expose KPI views for BI/Excel.

## Flow
1. `data/generate_dirty_data.py` -> generates sample dirty CSV (`data/sample/raw_orders.csv`)
2. `src/clean_orders.py` -> cleans fields and writes `output/clean_orders.csv` + `output/rejected_orders.csv`
3. `src/load_sqlite.py` -> loads valid rows into SQLite (`orders.db`)
4. `src/kpi_queries.sql` -> creates `v_kpi_by_status` and `v_kpi_by_customer`

## Quickstart
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python data\generate_dirty_data.py
python src\clean_orders.py
python src\load_sqlite.py
