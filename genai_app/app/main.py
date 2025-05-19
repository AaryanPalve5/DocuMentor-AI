from flask import Flask, request, jsonify

from ingestion import process_file
from chat_agent import chat_with_memory
from dashboard import generate_dashboard
from planner import auto_plan

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "<h2>✅ Gemini AI backend is running</h2>"

# Upload route (GET returns form, POST handles upload)
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return '''
        <h2>Upload File</h2>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required><br>
            <input type="text" name="user_id" placeholder="User ID" required><br>
            <input type="submit" value="Upload">
        </form>
        '''
    file = request.files.get("file")
    user_id = request.form.get("user_id", "default")

    if not file:
        return jsonify({"status": "error", "message": "No file provided"}), 400

    result = process_file(file, user_id)
    return jsonify(result)

# Chat route
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        return '''
        <h2>Gemini Chat</h2>
        <form method="post" action="/chat">
            <input type="text" name="user_id" placeholder="User ID" required><br>
            <textarea name="message" placeholder="Ask something..." required></textarea><br>
            <input type="submit" value="Chat">
        </form>
        '''
    user_id = request.form.get("user_id", "default")
    message = request.form.get("message")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    result = chat_with_memory(user_id, message)
    return jsonify(result)

# Dashboard route
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard_view():
    if request.method == "GET":
        return '''
        <h2>Load Dashboard</h2>
        <form method="post" action="/dashboard">
            <input type="text" name="user_id" placeholder="User ID" required><br>
            <input type="submit" value="Load Dashboard">
        </form>
        '''
    user_id = request.form.get("user_id", "default")
    result = generate_dashboard(user_id)
    return jsonify(result)

# Planner route
@app.route("/plan", methods=["GET", "POST"])
def plan():
    if request.method == "GET":
        return '''
        <h2>AI Planner</h2>
        <form method="post" action="/plan">
            <input type="text" name="user_id" placeholder="User ID" required><br>
            <textarea name="context" placeholder="Describe your objective..." required></textarea><br>
            <input type="submit" value="Generate Plan">
        </form>
        '''
    user_id = request.form.get("user_id", "default")
    context = request.form.get("context")

    if not context:
        return jsonify({"error": "Context is required"}), 400

    result = auto_plan(user_id, context)
    return jsonify(result)

# Run
if __name__ == "__main__":
    app.run(debug=True)
