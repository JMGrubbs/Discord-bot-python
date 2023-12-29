from flask import Flask, request, jsonify
from index import runGPT
from Redis.redis_cache import get_message, get_all_messages
from flask_cors import CORS

from env import api_config

# import json
API_KEY = api_config["agent_api"]["api_key"]
app = Flask(__name__)
CORS(app)


@app.route("/send_prompt", methods=["POST"])
def send_prompt():
    if request.headers.get("api-key") != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401
    # data example: { "assistant_id": "some-assistant-id", "message": "Hello, how are you?" }
    data = request.json
    assistant_id = data.get("assistant_id")
    input_message = data.get("message")
    if not assistant_id or not input_message:
        return jsonify({"error": "Assistant ID and message are required"}), 400

    try:
        response = runGPT(input_message)
        # response = "Request received"
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_response", methods=["POST"])
def get_prompt():
    if request.headers.get("api-key") != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401
    return jsonify({"response": get_message(request.json.get("message_id"))})


@app.route("/get_all_responses", methods=["POST"])
def get_all_responses():
    if request.headers.get("api-key") != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401

    return jsonify({"responses": get_all_messages()})


if __name__ == "__main__":
    app.run(debug=True)
