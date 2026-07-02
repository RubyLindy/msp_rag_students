from flask import Flask, request, jsonify, send_from_directory
from app.rag.pipeline import answer
import os
import json
import uuid
from datetime import datetime

# Create a logs folder if it doesn't exist
LOGS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOGS_FOLDER, exist_ok=True)

# Generate a unique file per session when the server starts
SESSION_ID = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + str(uuid.uuid4())[:8]
SESSION_LOG = os.path.join(LOGS_FOLDER, f"session_{SESSION_ID}.json")

# Initialise the file with an empty session
with open(SESSION_LOG, "w", encoding="utf-8") as f:
    json.dump({"session_id": SESSION_ID, "started": datetime.now().isoformat(), "exchanges": []}, f, indent=2)

app = Flask(__name__, static_folder="app/static")

DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "NAS")

@app.route("/")
def index():
    return send_from_directory("app/static", "chat-interface-rag.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or not data.get("message"):
        return jsonify({"error": "No message provided"}), 400

    user_message = data["message"]

    try:
        result = answer(user_message)

        # Save to session log
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "question": user_message,
            "answer": result["answer"],
            "sources": result["sources"]
        }
        with open(SESSION_LOG, "r+", encoding="utf-8") as f:
            session = json.load(f)
            session["exchanges"].append(exchange)
            f.seek(0)
            json.dump(session, f, indent=2, ensure_ascii=False)

        return jsonify({"response": result["answer"], "sources": result["sources"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/source-content", methods=["POST"])
def source_content():
    data = request.get_json()
    filename = data.get("filename", "")
    
    print(f"Raw filename received: '{filename}'")
    
    filename = os.path.basename(filename)
    print(f"After basename: '{filename}'")
 
    # Ensure it's a .md file inside the data folder
    if not filename.endswith(".md"):
        return jsonify({"error": "Invalid file type"}), 400
 
    filepath = os.path.join(DATA_FOLDER, filename)
    print(f"Full path: '{filepath}'")
    print(f"DATA_FOLDER: '{DATA_FOLDER}'")
    print(f"File exists: {os.path.isfile(filepath)}")

    if not os.path.isfile(filepath):
        return jsonify({"error": "File not found"}), 404
 
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    return jsonify({"filename": filename, "content": content})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

# Should probably add the contents of the sources within the first json chat response, instead of a separate function.
