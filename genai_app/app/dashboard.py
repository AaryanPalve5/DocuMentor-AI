import pandas as pd
import plotly.express as px
from memory_store import get_user_dataframe

def generate_dashboard(user_id):
    df = get_user_dataframe(user_id)
    if df is None or df.empty:
        return {"status": "error", "message": "No dashboard data"}

    charts = []
    try:
        if "Date" in df.columns and "Value" in df.columns:
            line_fig = px.line(df, x="Date", y="Value", title="Value Over Time")
            charts.append(line_fig.to_dict())

        bar_fig = px.bar(df.head(10), title="Top Records")
        charts.append(bar_fig.to_dict())

        table = df.head(20).to_dict(orient="records")
        return {"status": "success", "figures": charts, "table": table}
    except Exception as e:
        return {"status": "error", "message": str(e)}
