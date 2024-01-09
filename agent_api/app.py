from flask import Flask, request, jsonify
from index import main_operations
from flask_cors import CORS
from env import api_config
import asyncio


# from cache.RedisCache import get_message, get_all_messages
# import json
API_KEY = api_config["agent_api"]["api_key"]
app = Flask(__name__)
CORS(app)


@app.route("/prompt", methods=["POST"])
def send_prompt():
    if request.headers.get("api-key") != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401
    try:
        asyncio.run(main_operations.addMessage(request.json))
        response = main_operations.getResponse()
        return jsonify(response), 200
    except KeyError:
        return jsonify({"error": "Invalid message"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/messages", methods=["GET"])
def get_prompt():
    if request.headers.get("api-key") != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401
    try:
        response = main_operations.getResponse()
        print(response)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/deletemessages", methods=["DELETE"])
def delete_messages():
    if request.headers.get("api-key") != API_KEY:
        return jsonify({"error": "Invalid API key"}), 401

    try:
        response = main_operations.clearMessages()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
