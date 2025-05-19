import pandas as pd
import plotly.express as px
from memory_store import get_user_dataframe

def generate_dashboard(user_id):
    df = get_user_dataframe(user_id)
    if df is None or df.empty:
        return {"status": "error", "message": "No dashboard data"}

    try:
        figures = []
        if "Date" in df.columns and "Value" in df.columns:
            fig1 = px.line(df, x="Date", y="Value", title="Value Over Time")
            figures.append(fig1.to_dict())

        bar = px.bar(df.head(10), title="Top Records")
        figures.append(bar.to_dict())

        table = df.head(20).to_dict(orient="records")
        return {"status": "success", "figures": figures, "table": table}
    except Exception as e:
        return {"status": "error", "message": str(e)}
