from flask import Flask, request, jsonify
from index import addMessage, getMessages
from flask_cors import CORS
from env import api_config

# from cache.RedisCache import get_message, get_all_messages
# import json
API_KEY = api_config["agent_api"]["api_key"]
app = Flask(__name__)
CORS(app)


@app.route("/prompt", methods=["POST"])
def send_prompt():
    if request.headers.get("api-key") != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401
    # data example: { "assistant_id": "some-assistant-id", "message": "Hello, how are you?" }
    data = request.json
    package_type = data.get("package_type")
    if not package_type:
        return jsonify({"error": "package_type is required"}), 400

    if package_type == "agentprompt":
        print("BOOM", data)
        if addMessage(data["prompt"]):
            return jsonify({"status": "processing", "response": None}), 200
        return jsonify({"response": "Error"}), 405
    return jsonify({"error": "Invalid package_type"}), 400


@app.route("/messages", methods=["GET"])
def get_prompt():
    if request.headers.get("api-key") != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401
    return jsonify({"data": getMessages()}), 200


# @app.route("/get_all_responses", methods=["POST"])
# def get_all_responses():
#     if request.headers.get("api-key") != API_KEY:
#         return jsonify({"error": "Invalid API key"}), 401

#     return jsonify({"responses": get_all_messages()})


if __name__ == "__main__":
    app.run(debug=True)
