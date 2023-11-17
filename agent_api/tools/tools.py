from openai import OpenAI
import time
import json

# from getpass import getpass
from openai_tools import (
    create_gpt_thread,
    create_gpt_prompt,
    create_gpt_run,
    retrieve_gpt_run,
    get_gpt_prompt_response,
    cancel_gpt_run,
    conver_to_json,
    create_run_file,
)
import toml

RUNNING = True
OPENAI_API_KEY = toml.load("api_config.toml")["openai"]["api_key"]
client = client = OpenAI(
    api_key=OPENAI_API_KEY,
)
# Dictionary to hold multiple agents, keyed by assistant_id
agents = {
    "proxy_agent": {
        "name": "Naeblis",
        "assistant_id": toml.load("api_config.toml")["openai"]["naeblis"],
        "working": False,
        "user_proxy_thread": None,
        "proxy_agent_thread": None,
        "metadata": {
            "role": "user",
            "instructions": """As a user proxy agent, your responsibility is to streamline the dialogue between the user and specialized agents within this group chat. Your duty is to articulate user requests accurately to the relevant agents and maintain ongoing communication with them to guarantee the user's task is carried out to completion. Please do not respond to the user until the task is complete, an error has been reported by the relevant agent, or you are certain of your response.""",
        },
    },
    "assistant_agents": [
        {
            "name": "Kirk",
            "assistant_id": toml.load("api_config.toml")["openai"]["kirk"],
            "working": False,
            "thread": None,
            "metadata": {
                "role": "user",
                "instructions": "As a top-tier programming AI, you are adept at creating accurate Python scripts. You will properly name files and craft precise Python code with the appropriate imports to fulfill the user's request. Ensure to execute the necessary code before responding to the user.",
            },
        },
    ],
}


def get_completion(proxy_agent, input_message):
    input_message = input_message.lower()
    if input_message == "exit":
        print("Goodbye.")
        quit()

    if proxy_agent.get("user_proxy_thread") is None:
        proxy_agent["user_proxy_thread"] = create_gpt_thread(client)

    create_gpt_prompt(client, proxy_agent["user_proxy_thread"].id, input_message)
    run_gpt = create_gpt_run(
        client, proxy_agent["user_proxy_thread"].id, proxy_agent["assistant_id"]
    )
    tries = 0
    while run_gpt.status != "completed" and run_gpt.status != "failed":
        time.sleep(3)
        tries += 1
        run_gpt = retrieve_gpt_run(client, proxy_agent["user_proxy_thread"].id, run_gpt.id)
        print(run_gpt.status)
        if tries > 25:
            print("Error: GPT run took too long.")
            run_gpt = cancel_gpt_run(client, proxy_agent["user_proxy_thread"].id, run_gpt.id)
            print(run_gpt)
            break

    response = get_gpt_prompt_response(client, proxy_agent["user_proxy_thread"].id)
    print(response)
    try:
        response = conver_to_json(str(response[7:-3]))
    except Exception as e:
        print(e)

    new_file_output = create_run_file(response)
    print(new_file_output)

    get_completion(proxy_agent, input("Enter a message: "))


if __name__ == "__main__":
    get_completion(agents.get("proxy_agent"), input("Enter a message: "))
