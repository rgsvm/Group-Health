import pandas as pd
import sqlite3
import json

DB_PATH = "sleep_dashboard.db"

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM sleep_screen", conn)
conn.close()

print(df.columns)
print(df.head())

if "Value" in df.columns:
    def extract_bpm(x):
        try:
            if isinstance(x, str) and x.strip().startswith("{"):
                return json.loads(x).get("bpm")
        except:
            return None
        return None

    df["bpm"] = df["Value"].apply(extract_bpm)

print(df.describe(include="all"))
