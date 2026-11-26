import sqlite3
import pandas as pd
from .config import DATA_DIR

DB_PATH = DATA_DIR / "abc_hr.db"

def save_dataframe(df: pd.DataFrame):
    # SQLite table is refreshed whenever a new CSV is uploaded.
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql("hr_employees", conn, if_exists="replace", index=False)

def get_database_info():
    with sqlite3.connect(DB_PATH) as conn:
        count = conn.execute("SELECT COUNT(*) FROM hr_employees").fetchone()[0]
    return {"database": str(DB_PATH.name), "table": "hr_employees", "rows": count}
