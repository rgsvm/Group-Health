import pandas as pd
import sqlite3
import json
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from llm_summary import generate_summary

DB_PATH = "sleep_dashboard.db"

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sleep_screen", conn)
    conn.close()
    return df

df = load_data()

if "Time" in df.columns:
    df["Time"] = pd.to_numeric(df["Time"], errors="coerce")
if "Value" in df.columns:
    def extract_bpm(x):
        try:
            if isinstance(x, str) and x.strip().startswith("{"):
                return json.loads(x).get("bpm")
        except:
            return None
        return None
    df["bpm"] = df["Value"].apply(extract_bpm)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Sleep Recovery Dashboard"),
    dcc.Dropdown(
        id="metric",
        options=[
            {"label": "Heart Rate", "value": "bpm"},
            {"label": "Sleep Rating", "value": "sleep_rating"}
        ],
        value="bpm"
    ),
    dcc.Graph(id="trend"),
    html.Button("Generate AI Summary", id="btn", n_clicks=0),
    html.Div(id="summary")
])

@app.callback(
    Output("trend", "figure"),
    Input("metric", "value")
)
def update_chart(metric):
    if metric not in df.columns:
        return px.line(title="Metric not available")
    plot_df = df.dropna(subset=[metric]).copy()
    if "Time" in plot_df.columns:
        plot_df = plot_df.sort_values("Time")
    fig = px.line(plot_df, y=metric, title=f"{metric} trend")
    return fig

@app.callback(
    Output("summary", "children"),
    Input("btn", "n_clicks")
)
def update_summary(n):
    if n == 0:
        return "Click to generate an AI summary."
    metrics = {
        "rows": len(df),
        "columns": list(df.columns),
        "avg_sleep_rating": float(df["sleep_rating"].dropna().mean()) if "sleep_rating" in df.columns else None,
        "avg_bpm": float(df["bpm"].dropna().mean()) if "bpm" in df.columns else None
    }
    try:
        text = generate_summary(metrics)
        return html.Pre(text)
    except Exception as e:
        return f"OpenAI summary unavailable: {e}"

if __name__ == "__main__":
    app.run_server(debug=True)
