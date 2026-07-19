from pathlib import Path
import sqlite3
import pandas as pd

def save_transactions(db_file: Path, transactions: pd.DataFrame) -> None:
    db_file.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_file) as conn:
        transactions.to_sql("transactions", conn, if_exists="replace", index=False)

def load_transactions(db_file: Path) -> pd.DataFrame:
    with sqlite3.connect(db_file) as conn:
        return pd.read_sql_query("SELECT * FROM transactions", conn)
