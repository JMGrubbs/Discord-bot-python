from flask import Flask, request, jsonify
from agentclass import Agents
import toml

# import json

app = Flask(__name__)

# Dictionary to hold multiple agents, keyed by assistant_id
agents = {}


def get_or_create_agent(assistant_id):
    if assistant_id not in agents:
        agents[assistant_id] = Agents()
    return agents[assistant_id]


@app.route("/send_prompt", methods=["POST"])
def send_prompt():
    if request.headers["api_key"] != toml.load("config.toml")["agent_api"]["api_key"]:
        return jsonify({"error": "Invalid API key"}), 401
    # data example: { "assistant_id": "some-assistant-id", "message": "Hello, how are you?" }
    data = request.json
    assistant_id = data.get("assistant_id")
    input_message = data.get("message")

    if not assistant_id or not input_message:
        return jsonify({"error": "Assistant ID and message are required"}), 400

    agent = get_or_create_agent(assistant_id)
    response = agent.run_gpt(input_message)
    return jsonify({"response": response})


@app.route("/get_response", methods=["GET"])
def get_response():
    if request.headers["api_key"] != toml.load("config.toml")["agent_api"]["api_key"]:
        return jsonify({"error": "Invalid API key"}), 401
    assistant_id = request.args.get("assistant_id")

    if not assistant_id:
        return jsonify({"error": "Assistant ID is required"}), 400

    if assistant_id in agents:
        response = agents[assistant_id].get_gpt_latest_response()
        return jsonify({"response": response})
    else:
        return jsonify({"error": "Agent not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
