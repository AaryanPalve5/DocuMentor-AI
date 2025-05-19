import pandas as pd
import pickle
import os

memory_dir = "../vector_store/memory/"
os.makedirs(memory_dir, exist_ok=True)

user_dataframes = {}

def store_user_data(user_id, text):
    df = pd.DataFrame([{"Text": text}])
    user_dataframes[user_id] = df

def get_user_dataframe(user_id):
    return user_dataframes.get(user_id)

def store_plan(user_id, plan):
    with open(os.path.join(memory_dir, f"{user_id}_plan.pkl"), "wb") as f:
        pickle.dump(plan, f)

def get_plan(user_id):
    try:
        with open(os.path.join(memory_dir, f"{user_id}_plan.pkl"), "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []
