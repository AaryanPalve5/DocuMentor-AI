from flask import Flask, request, render_template, jsonify
from ingestion import process_file
from chat_agent import chat_with_memory
from dashboard import generate_dashboard
from planner import auto_plan

app = Flask(__name__)

@app.route("/")
def index():
    return "Generative AI Backend is running."

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    user_id = request.form.get("user_id", "default")
    result = process_file(file, user_id)
    return jsonify(result)

@app.route("/chat", methods=["POST"])
def chat():
    user_id = request.form.get("user_id", "default")
    message = request.form.get("message")
    result = chat_with_memory(user_id, message)
    return jsonify(result)

@app.route("/dashboard", methods=["POST"])
def dashboard_view():
    user_id = request.form.get("user_id", "default")
    result = generate_dashboard(user_id)
    return jsonify(result)

@app.route("/plan", methods=["POST"])
def plan():
    user_id = request.form.get("user_id", "default")
    context = request.form.get("context")
    result = auto_plan(user_id, context)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
