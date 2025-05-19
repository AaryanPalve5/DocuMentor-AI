from datetime import datetime, timedelta
from memory_store import store_plan

def auto_plan(user_id, context):
    today = datetime.now()
    plan = []

    for i in range(7):
        day = today + timedelta(days=i)
        plan.append({
            "date": day.strftime("%Y-%m-%d"),
            "task": f"Review: '{context[:50]}...'"
        })

    store_plan(user_id, plan)
    return {"status": "success", "plan": plan}
