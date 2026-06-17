import pandas as pd
import sqlite3

CSV_PATH = "data/GroupHealth_SleepScreen.csv"
DB_PATH = "sleep_dashboard.db"

df = pd.read_csv(CSV_PATH)

conn = sqlite3.connect(DB_PATH)
df.to_sql("sleep_screen", conn, if_exists="replace", index=False)
conn.close()

print(f"Loaded {len(df)} rows into SQLite")
