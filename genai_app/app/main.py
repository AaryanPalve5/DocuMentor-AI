from flask import Flask, render_template, request, jsonify
from ingestion import process_file
from chat_agent import chat_with_memory      # returns dict {"response": ...}
# from dashboard import generate_dashboard    # returns dict {'figures':…, 'table':…}
from planner import auto_plan               # returns dict {'status':…, 'plan':…}

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """
    Home landing page. Renders the Upload screen.
    """
    return render_template("index.html")


# Upload route (GET shows form, POST processes file)
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        # Show upload form
        return render_template("index.html")
    
    # Handle file upload
    user_id = request.form.get("user_id", "default")
    file = request.files.get("file")
    if not file:
        return jsonify({"status": "error", "message": "No file provided"}), 400

    result = process_file(file, user_id)
    # Re-render the form with the extraction result
    return render_template("index.html", upload_result=result)


# Chat route (GET shows chat UI, POST sends message)
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        # Show chat form
        return render_template("chat.html")
    
    user_id = request.form.get("user_id", "default")
    message = request.form.get("message", "").strip()
    if not message:
        # Show error on page if no message
        return render_template("chat.html", error="Message is required")

    result = chat_with_memory(user_id, message)  
    return render_template(
        "chat.html",
        user_id=user_id,
        message=message,
        response=result.get("response")
    )


# Dashboard route (GET shows selector, POST renders charts/table)
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard_view():
    if request.method == "GET":
        # Initially no data
        return render_template("dashboard.html", figures=None, table=None)
    
    user_id = request.form.get("user_id", "default")
    data = generate_dashboard(user_id) 
    return render_template(
        "dashboard.html",
        figures=data.get("figures"),
        table=data.get("table")
    )


# Planner route (GET shows planner UI, POST generates plan)
@app.route("/plan", methods=["GET", "POST"])
def plan():
    if request.method == "GET":
        # Show planner form
        return render_template("planner.html", plan=None)
    
    user_id = request.form.get("user_id", "default")
    context = request.form.get("context", "").strip()
    if not context:
        return render_template("planner.html", error="Context is required")

    result = auto_plan(user_id, context)
    return render_template("planner.html", plan=result.get("plan"))


if __name__ == "__main__":
    # Ensure Flask reloads on code changes
    app.run(debug=True, host="0.0.0.0", port=5000)
