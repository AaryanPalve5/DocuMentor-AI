from flask import Blueprint, render_template, request
import plotly.express as px
from .memory_store import get_user_data

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """
    Build Plotly figures for numeric columns and render pure HTML
    in templates/dashboard.html.
    """
    user_id = request.form.get('user_id', 'default')
    df = get_user_data(user_id)
    figures = []
    table = df.to_dict(orient='records') if not df.empty else []

    for col in df.select_dtypes(include=['number']).columns:
        fig = px.bar(df, x=df.index, y=col, title=col)
        figures.append(fig)

    return render_template('dashboard.html', figures=figures, table=table)
