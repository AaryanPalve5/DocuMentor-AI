from flask import Flask, request, jsonify
from ingestion import process_file
from chat_agent import chat_with_memory
from dashboard import generate_dashboard
from planner import auto_plan

app = Flask(__name__)

@app.route("/")
def index():
    return "Generative AI Backend is running."

# Allow both GET and POST so you can browse to /upload for a quick form
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        # Simple HTML form for manual testing
        return """
        <h1>Upload a File</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
          <input type="text" name="user_id" placeholder="user_id" required><br>
          <input type="file" name="file" required><br>
          <button type="submit">Upload</button>
        </form>
        """, 200

    # POST handling
    file = request.files.get("file")
    if not file:
        return jsonify({"status": "error", "message": "No file provided"}), 400

    user_id = request.form.get("user_id", "default")
    try:
        result = process_file(file, user_id)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify(result)

@app.route("/chat", methods=["POST"])
def chat():
    user_id = request.form.get("user_id", "default")
    message = request.form.get("message", "")
    if not message:
        return jsonify({"status": "error", "message": "No message provided"}), 400

    try:
        result = chat_with_memory(user_id, message)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify(result)

@app.route("/dashboard", methods=["POST"])
def dashboard_view():
    user_id = request.form.get("user_id", "default")
    try:
        result = generate_dashboard(user_id)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify(result)

@app.route("/plan", methods=["POST"])
def plan():
    user_id = request.form.get("user_id", "default")
    context = request.form.get("context", "")
    if not context:
        return jsonify({"status": "error", "message": "No context provided"}), 400

    try:
        result = auto_plan(user_id, context)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
