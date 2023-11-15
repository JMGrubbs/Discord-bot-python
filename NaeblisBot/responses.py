import requests
import toml


def handle_responses(p_message, assistant_id):
    try:
        url = toml.load("config.toml")["agent_api"]["url"] + "/send_prompt"
        api_key = toml.load("config.toml")["agent_api"]["api_key"]
        headers = {"api-key": api_key, "Content-Type": "application/json"}
        payload = {"assistant_id": str(assistant_id), "message": str(p_message)}
        response = requests.post(
            url,
            headers=headers,
            json=payload,
        )
        data = response.json()
        return data.get("response")
    except Exception as e:
        error = f"Api Call Failed with ERROR: {e}"
        print(error)
