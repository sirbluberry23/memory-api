from flask import Flask, request, jsonify
from datetime import datetime
import uuid
import json
import os

app = Flask(__name__)

MEMORY_FILE = "memories.json"


# ---------------------------------------------------
# Load saved memories from file
# ---------------------------------------------------
def load_memories():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)
                return {m["id"]: m for m in data}
        except:
            return {}
    return {}


# ---------------------------------------------------
# Save memories to file
# ---------------------------------------------------
def save_memories_to_file():
    with open(MEMORY_FILE, "w") as f:
        json.dump(list(memories.values()), f, indent=2)


# in-memory dictionary (restored from file at startup)
memories = load_memories()


# ---------------------------------------------------
# List all memories
# ---------------------------------------------------
@app.route("/memory", methods=["GET"])
def list_memories():
    return jsonify(list(memories.values()))


# ---------------------------------------------------
# Save new memory
# ---------------------------------------------------
@app.route("/memory", methods=["POST"])
def save_memory():
    data = request.json
    if not data or "content" not in data:
        return jsonify({"error": "Missing content"}), 400

    memory_id = str(uuid.uuid4())
    memory = {
        "id": memory_id,
        "content": data["content"],
        "createdAt": datetime.utcnow().isoformat()
    }

    memories[memory_id] = memory
    save_memories_to_file()   # persist to file

    return jsonify(memory), 201


@app.route("/memory", methods=["DELETE"])
def delete_memory_by_content():
    data = request.json
    if not data or "content" not in data:
        return jsonify({"error": "content field required"}), 400

    target = data["content"].lower()
    to_delete = None

    for mem_id, mem in memories.items():
        if target in mem["content"].lower():
            to_delete = mem_id
            break

    if to_delete:
        del memories[to_delete]
        save_memories_to_file()
        return jsonify({"status": "deleted"}), 200

    return jsonify({"error": "Not found"}), 404




# ---------------------------------------------------
# Start server
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
