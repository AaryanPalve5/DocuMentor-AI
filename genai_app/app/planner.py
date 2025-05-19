from datetime import datetime, timedelta
from config import GEMINI_API_KEY
import google.generativeai as genai
from memory_store import store_plan
import json
import re

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def auto_plan(user_id, context):
    today = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""
You are an AI productivity assistant.

Create a 7-day schedule starting from today ({today}) for the following goal:

"{context}"

Output strictly a JSON array like:
[
  {{"date": "YYYY-MM-DD", "task": "Task description"}},
  ...
]

Do not include markdown or explanations.
"""

    try:
        # Use Gemini 1.5 Flash (or fallback to gemini-pro if needed)
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            contents=[{"role": "user", "parts": [prompt]}]
        )

        text = response.text.strip()

        # Clean output if wrapped in markdown ```json blocks
        cleaned = re.sub(r"^```(json)?|```$", "", text, flags=re.MULTILINE).strip()

        plan = json.loads(cleaned)

        # Validate basic structure
        if not isinstance(plan, list) or not all("date" in d and "task" in d for d in plan):
            raise ValueError("Invalid JSON structure returned by Gemini")

        store_plan(user_id, plan)
        return {"status": "success", "plan": plan}

    except Exception as e:
        print(f"[Planner Fallback] Gemini failed: {e}")
        # Simple fallback: 7-day dummy plan
        fallback = [
            {
                "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                "task": f"Day {i+1}: {context}"
            }
            for i in range(7)
        ]
        store_plan(user_id, fallback)
        return {"status": "fallback", "plan": fallback}
