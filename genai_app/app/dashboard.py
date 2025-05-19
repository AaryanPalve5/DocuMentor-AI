import pandas as pd
import plotly.express as px
from memory_store import get_user_dataframe

def generate_dashboard(user_id):
    df = get_user_dataframe(user_id)
    if df is None or df.empty:
        return {"status": "error", "message": "No dashboard data"}

    try:
        figures = []

        # Line chart if Date and Value present
        if "Date" in df.columns and "Value" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df.dropna(subset=["Date"], inplace=True)
            fig1 = px.line(df, x="Date", y="Value", title="Value Over Time")
            figures.append(fig1.to_plotly_json())  # ✅ JSON-safe format

        # Bar chart
        fig2 = px.bar(df.head(10), title="Top 10 Records")
        figures.append(fig2.to_plotly_json())  # ✅ Safe for jsonify

        # Table conversion: convert all non-serializable items (like np.int64) to built-ins
        table_data = df.head(20).copy()
        table = table_data.astype(str).to_dict(orient="records")

        return {
            "status": "success",
            "figures": figures,
            "table": table
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
