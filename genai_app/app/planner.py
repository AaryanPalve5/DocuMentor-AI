from datetime import datetime, timedelta
from config import GEMINI_API_KEY
import google.generativeai as genai
from memory_store import store_plan

genai.configure(api_key=GEMINI_API_KEY)

def auto_plan(user_id, context):
    prompt = f"""
You are an AI task planner. Based on this input: "{context}",
create a 7-day schedule in JSON format with "date" and "task".
Start today.
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(prompt)

    # Expect result.text to contain a list of dicts
    import json
    try:
        plan = json.loads(result.text)
    except:
        plan = [{"date": (datetime.now()+timedelta(days=i)).strftime("%Y-%m-%d"), "task": f"Day {i+1}: {context}"} for i in range(7)]

    store_plan(user_id, plan)
    return {"status": "success", "plan": plan}
