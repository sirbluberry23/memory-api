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
    memory_id = str(uuid.uuid4())
    memory = {
        "id": memory_id,
        "content": data["content"],
        "createdAt": datetime.utcnow().isoformat()
    }
    memories[memory_id] = memory
    return jsonify(memory), 201

@app.route("/memory/<id>", methods=["GET"])
def get_memory(id):
    memory = memories.get(id)
    if memory:
        return jsonify(memory)
    return jsonify({"error": "Not found"}), 404

@app.route("/memory", methods=["DELETE"])
def delete_memory_by_content():
    data = request.json
    content = data.get("content")

    if not content:
        return jsonify({"error": "content field required"}), 400

    to_delete = None
    for key, mem in memories.items():
        if mem["content"] == content:
            to_delete = key
            break

    if to_delete:
        del memories[to_delete]
        return '', 204

    return jsonify({"error": "Not found"}), 404
