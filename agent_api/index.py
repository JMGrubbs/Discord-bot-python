from openai import OpenAI
import agentClassv2

# from getpass import getpass
# from openai_tools import (
#     create_run_file,
#     get_completion,
# )
import toml

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
            "instructions": """
            You are a user agent proxy. You are to give instructions to an assitant coding agent to complete a coding task based on the prompt given to you. The assistant coding agent will write code to complete the task based on your instructions. You are not to write the code yourself. You are only to give instructions to the assitant coding agent.
            Instructions:
                1. Create completion standards for a the coding coding task given to you.
                2. Give completion stadards for the coding task to the assitsant coding agent to use when writing code.
                3. Do not try to accomplish this task yourself. You are only to give instructions to the assitant coding agent.
                4. if the output of the assistant coding agent does not meet the completion standards, give the assistant coding agent new instructions to complete the task.
                5. If the output of the assistant coding agent meets the completion standards return a json object with the following keys:
                    "completed" as true or false
                    "messege_to_user" as a string
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
                    5. the response code should be enclosed in an exporable function.

                The JSON object can have any number of key value pairs but must include the 3 keys above. The python code can be any valid python code in the form of a string that can be parsed by json.loads(). The filename can be any valid filename in string format. The instructions can be any valid string.
                Example response: "{"code": "print('Hello world')", "filename": "hello.py", "Instructions": "print hello world"}" """,
            },
        },
    ],
}
model = "gpt-3.5-turbo-1106"
proxy_agent_naeblis = agentClassv2.Agents(
    agentName=agents.get("proxy_agent").get("name"),
    instructions=agents.get("proxy_agent").get("metadata").get("instructions"),
    agentID=agents.get("proxy_agent").get("assistant_id"),
    model=model,
)

assistant_agent = agentClassv2.Agents(
    agentName=agents.get("assistant_agents")[0].get("name"),
    instructions=agents.get("assistant_agents")[0].get("metadata").get("instructions"),
    agentID=agents.get("assistant_agents")[0].get("assistant_id"),
    model=model,
)

print(proxy_agent_naeblis.getAgentID())

quit()


def runGPT(input_message):
    input_message = input_message.lower()
    if input_message == "exit":
        print("Goodbye.")
        quit()

    proxy_agent_naeblis.get_completion(client, input_message)


if __name__ == "__main__":
    runGPT(input("Enter a message: "))
