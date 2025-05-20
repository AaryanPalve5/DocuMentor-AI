# planner.py
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request
import google.generativeai as genai
from config import GEMINI_API_KEY
from memory_store import store_plan
import json
import re

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

planner_bp = Blueprint('planner', __name__, template_folder='templates')

def auto_plan(user_id: str, context: str) -> dict:
    """
    Use Gemini to generate a 7-day JSON plan; fallback to a dummy plan on error.
    """
    today = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""
You are an AI productivity assistant.

Create a 7-day schedule starting from today ({today}) for the following goal:

\"{context}\"

Output strictly a JSON array like:
[
  {{"date": "YYYY-MM-DD", "task": "Task description"}},
  ...
]

Do not include markdown or explanations.
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(contents=[{"role": "user", "parts": [prompt]}])
        text = response.text.strip()

        # Remove any ```json fences
        cleaned = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
        plan = json.loads(cleaned)

        if not isinstance(plan, list) or not all("date" in d and "task" in d for d in plan):
            raise ValueError("Invalid JSON structure")

        store_plan(user_id, plan)
        return {"status": "success", "plan": plan}

    except Exception as e:
        print(f"[Planner Fallback] Gemini failed: {e}")
        # Fallback dummy plan
        fallback = [
            {
                "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                "task": f"Day {i+1}: {context}"
            }
            for i in range(7)
        ]
        store_plan(user_id, fallback)
        return {"status": "fallback", "plan": fallback}

@planner_bp.route('/plan', methods=['GET', 'POST'])
def plan():
    """
    GET: render planner.html with no plan.
    POST: call auto_plan and render planner.html with the resulting plan.
    """
    plan_items = None
    error = None

    if request.method == 'POST':
        user_id = request.form.get('user_id', '')
        context = request.form.get('context', '').strip()

        if not user_id or not context:
            error = "User ID and context are required."
        else:
            result = auto_plan(user_id, context)
            plan_items = result.get("plan")

    return render_template('planner.html', plan=plan_items, error=error)
