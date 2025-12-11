from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)
memories = {}

@app.route("/memory", methods=["GET"])
def list_memories():
    return jsonify(list(memories.values()))

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
    return jsonify(memory), 201

@app.route("/memory", methods=["DELETE"])
def delete_memory_by_content():
    data = request.json
    if not data or "content" not in data:
        return jsonify({"error": "content field required"}), 400

    target = data["content"]
    to_delete = None

    for mem_id, mem in memories.items():
        if mem["content"] == target:
            to_delete = mem_id
            break

    if to_delete:
        del memories[to_delete]
        return '', 204

    return jsonify({"error": "Not found"}), 404
