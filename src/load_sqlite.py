from pathlib import Path
import sqlite3
import pandas as pd


def load_to_sqlite(csv_path: Path, db_path: Path, table_name: str = "clean_orders") -> None:
    if not csv_path.exists():
        raise FileNotFoundError(f"File non trovato: {csv_path}. Esegui prima src/clean_orders.py.")

    df = pd.read_csv(csv_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

    print(f"Caricate {count} righe nella tabella '{table_name}' in {db_path}")


if __name__ == "__main__":
    load_to_sqlite(
        csv_path=Path("output/clean_orders.csv"),
        db_path=Path("orders.db"),
    )
