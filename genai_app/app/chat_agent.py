import google.generativeai as genai
from flask import Blueprint, render_template, request
from config import GEMINI_API_KEY
from memory_store import get_chat_history, update_chat_history
from utils import retrieve_relevant_chunks

# Configure Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

chat_bp = Blueprint('chat', __name__, template_folder='templates')

def chat_with_memory(user_id: str, message: str) -> dict:
    """
    Pull context and history, call Gemini, update history, return response.
    """
    # 1) Get prior chat history
    history = get_chat_history(user_id)
    # 2) Get relevant chunks for context
    context = retrieve_relevant_chunks(user_id, message)

    # 3) Build prompt
    prompt = f"""
You are an AI assistant. Use the following context and conversation history to answer the user:

Context:
{context}

History:
{history}

User: {message}
"""

    # 4) Call Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(contents=[{"role": "user", "parts": [prompt]}])
    ai_text = response.text.strip()

    # 5) Store in history
    update_chat_history(user_id, message, ai_text)

    return {"response": ai_text}

@chat_bp.route('/chat', methods=['GET', 'POST'])
def chat():
    """
    GET: render chat.html
    POST: process form, call chat_with_memory, render chat.html with results
    """
    user_id = ""
    message = ""
    ai_resp = None
    error = None

    if request.method == 'POST':
        user_id = request.form.get('user_id', '').strip()
        message = request.form.get('message', '').strip()

        if not user_id or not message:
            error = "User ID and message are required."
        else:
            result = chat_with_memory(user_id, message)
            ai_resp = result.get("response")

    return render_template(
        'chat.html',
        user_id=user_id,
        message=message,
        response=ai_resp,
        error=error
    )