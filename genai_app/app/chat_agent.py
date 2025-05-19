import google.generativeai as genai
from config import GEMINI_API_KEY
from memory_store import get_chat_history, update_chat_history
from utils import retrieve_relevant_chunks

genai.configure(api_key=GEMINI_API_KEY)

def chat_with_memory(user_id, message):
    history = get_chat_history(user_id)
    context = retrieve_relevant_chunks(user_id, message)

    prompt = f"""
You are an AI assistant. Use the following context and conversation history to answer the user:

Context:
{context}

History:
{history}

User: {message}
"""

    model = genai.GenerativeModel("gemini-1.5-flash")

    # generate_content automatically wraps the text internally
    response = model.generate_content(prompt)

    update_chat_history(user_id, message, response.text)
    return {"response": response.text}
