from openai import OpenAI
import time

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
            "instructions": """Instructions:
                1. Create completion standards for a the coding coding task given to you.
                2. Give completion stadards for the coding task to the assitsant coding agent to use when writing code.
                3. If the new file exucuted works as intended return "success" otherwise return reiterate and improved instructions for the assitsant coding agent
                4. Do not try to accomplish this task yourself. You are only to give instructions to the assitant coding agent.
            """,
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
                "instructions": """Instructions:
                    1. Responsed with ONLY a valid json object in the form of a string "{object}"
                    2. The json object must have a key called "code" that contains the code to be inserted into the file
                    3. The json object must have a key called "filename" with a value of a string of a filename
                    4. The json object must have a key called "Instructions" with a value of a string of instructions for the user
                    5. The python code must print "Hello world"

                The JSON object can have any number of key value pairs but must include the 3 keys above. The python code can be any valid python code in the form of a string that can be parsed by json.loads(). The filename can be any valid filename in string format. The instructions can be any valid string.
                Example response: "{"code": "print('Hello world')", "filename": "hello.py", "Instructions": "print hello world"}" """,
            },
        },
    ],
}


def run_gpt(input_message):
    input_message = input_message.lower()
    if input_message == "exit":
        print("Goodbye.")
        quit()

    user_proxy_response = get_completion(agents.get("proxy_agent"), input_message)
    print("Naeblis_user_proxy: ", user_proxy_response)
    new_file_output = None
    working = True
    while working:
        print("Working...")
        assistant_response = get_completion(agents.get("assistant_agents")[0], user_proxy_response)
        print("Kirk_assistant_response:", assistant_response)
        response_json = conver_to_json(str(assistant_response))

        new_file_output = create_run_file(response_json)

        user_proxy_response = get_completion(agents.get("proxy_agent"), str(new_file_output))
        if "success" in str(user_proxy_response).lower():
            working = False

    print("Success")
    print(user_proxy_response)
    run_gpt(input("Ready for next task: "))


def get_completion(proxy_agent, input_message):
    if proxy_agent.get("user_proxy_thread") is None:
        proxy_agent["user_proxy_thread"] = create_gpt_thread(client)

    create_gpt_prompt(client, proxy_agent["user_proxy_thread"].id, input_message)
    run_gpt = create_gpt_run(client, proxy_agent["user_proxy_thread"].id, proxy_agent)
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

    return get_gpt_prompt_response(client, proxy_agent["user_proxy_thread"].id)


if __name__ == "__main__":
    run_gpt(input("Enter a message: "))
