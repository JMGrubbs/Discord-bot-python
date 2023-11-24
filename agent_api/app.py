from flask import Flask, request, jsonify
import toml
from index import runGPT

# import json
API_KEY = toml.load("api_config.toml")["agent_api"]["api_key"]
app = Flask(__name__)


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
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
