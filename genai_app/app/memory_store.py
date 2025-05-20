import os
import pickle
import pandas as pd

# Directory for persisting plans/chat history, etc.
memory_dir = os.path.join("..", "vector_store", "memory")
os.makedirs(memory_dir, exist_ok=True)

# In‑memory stores
user_dataframes = {}   # user_id -> pandas.DataFrame
chat_histories = {}    # user_id -> list of chat strings

def store_user_data(user_id: str, data):
    """
    Store a DataFrame directly, or wrap text into a one-column DataFrame.
    """
    if isinstance(data, pd.DataFrame):
        user_dataframes[user_id] = data
    else:
        df = pd.DataFrame([{"Text": data}])
        user_dataframes[user_id] = df

def get_user_data(user_id: str) -> pd.DataFrame:
    """
    Retrieve the stored DataFrame for a user, or an empty one.
    """
    return user_dataframes.get(user_id, pd.DataFrame())

def store_plan(user_id: str, plan):
    """
    Persist a plan (e.g., list of dicts) to disk via pickle.
    """
    path = os.path.join(memory_dir, f"{user_id}_plan.pkl")
    with open(path, "wb") as f:
        pickle.dump(plan, f)

def load_plan(user_id: str):
    """
    Load a persisted plan if it exists, else return None.
    """
    path = os.path.join(memory_dir, f"{user_id}_plan.pkl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None

def update_chat_history(user_id: str, user_msg: str, ai_resp: str):
    """
    Append a round of chat to in‑memory history.
    """
    chat_histories.setdefault(user_id, [])
    chat_histories[user_id].append(f"User: {user_msg}\nAI: {ai_resp}")

def get_chat_history(user_id: str) -> str:
    """
    Return the entire conversation as a single string.
    """
    return "\n".join(chat_histories.get(user_id, []))
