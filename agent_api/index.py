from openai import OpenAI
import AgentClass
import AgentToolsClass
import toml

OPENAI_API_KEY = toml.load("api_config.toml")["openai"]["api_key"]
client = client = OpenAI(
    api_key=OPENAI_API_KEY,
)

# agents dicunaary to hold multiple agents, keyed by assistant_id
agents = {
    "proxy_agent": {
        "name": "Naeblis",
        "assistant_id": toml.load("api_config.toml")["openai"]["naeblis"],
        "working": False,
        "metadata": {
            "role": "user",
            "instructions": """
                You are a user agent proxy. You are to give instructions to an assitant coding agent to complete a coding task based on the prompt given to you. The assistant coding agent will write code to complete the task based on your instructions. You are not to write the code yourself. You are only to give instructions to the assitant coding agent.
                Instructions:
                    1. Create completion standards for a the coding task given to you.
                    2. Give completion stadards for the coding task to the assitsant coding agent to use when writing code.
                    3. Do not try to accomplish this task yourself. You are only to give instructions to the assitant coding agent.
                    4. if the output of the assistant coding agent does not meet the completion standards, give the assistant coding agent new instructions to complete the task.
                    5. If the output of the assistants agents newly created script meets the completion standards return a json object with the following keys: "completed" as true or false, and "messege_to_user" as a string
                    6. return only a json object with the following keys: "completed" as true or false, and "messege_to_user" as a string
                """,
        },
    },
    "assistant_agents": {
        "name": "Kirk",
        "assistant_id": toml.load("api_config.toml")["openai"]["kirk"],
        "metadata": {
            "role": "user",
            "instructions": """
                    Instructions:
                        1. Your response must be in the form of a json object
                        2. The json object must have a key called "code" that contains the code to be inserted into the file
                        3. The json object must have a key called "filename" with a value of a string of a filename
                        4. The json object must have a key called "Instructions" with a value of a string of instructions for the user

                    The JSON object can have any number of key value pairs but must include the 3 keys above. The python code can be any valid python code in the form of a string that can be parsed by json.loads(). The filename can be any valid filename in string format. The instructions can be any valid string.
                    Example response: "{"code": "print('Hello world')", "filename": "hello.py", "Instructions": "print hello world"}"
                """,
        },
    },
    "testing_agents": {
        "name": "Alexander",
        "assistant_id": toml.load("api_config.toml")["openai"]["alexander"],
        "metadata": {
            "role": "user",
            "instructions": """
                You are a code testing agent. When called you need to write a test for the code that the assistant agent creates.
                Instructions:
                    1. Create a test for the code that the assistant agent creates.
                    2. You will import the script that the assistant agent creates, call the function and return the output.
                    3. You will return the output of the test in the form of a json object with the following keys: "output" as a string of the output of the test
                    4. you will be given a json object with the code and with the code and file name you need to write the test for
                    5. Responed with only a json object
            """,
        },
    },
}

# runtime setup
model = "gpt-3.5-turbo-1106"
proxy_agent_naeblis = AgentClass.Agents(
    agentName=agents.get("proxy_agent").get("name"),
    instructions=agents.get("proxy_agent").get("metadata").get("instructions"),
    agentID=agents.get("proxy_agent").get("assistant_id"),
    model=model,
)

assistant_agent = AgentClass.Agents(
    agentName=agents.get("assistant_agents").get("name"),
    instructions=agents.get("assistant_agents").get("metadata").get("instructions"),
    agentID=agents.get("assistant_agents").get("assistant_id"),
    model=model,
)

tesing_agent = AgentClass.Agents(
    agentName=agents.get("testing_agents").get("name"),
    instructions=agents.get("testing_agents").get("metadata").get("instructions"),
    agentID=agents.get("testing_agents").get("assistant_id"),
    model=model,
)

agent_tools = AgentToolsClass.AgentTools(
    workspace="tools/agent_workspace/", tools="tools/agent_tools/"
)


def runGPT(input_message):
    input_message = input_message.lower()
    if input_message == "exit":
        print("Goodbye.")
        quit()

    user_proxy_response = proxy_agent_naeblis.get_completion(client, input_message)
    print("Naeblis_user_proxy: ", user_proxy_response)
    while True:
        print("Working...")
        # the below code is gets coding assistants response to the user proxy agents prompt
        assistant_agent_response = assistant_agent.get_completion(client, user_proxy_response)
        print("Kirk_assistant_response:", assistant_agent_response)

        # the below code is for creating a new script from the coding assistants response
        json_object = agent_tools.getjson(json_object_string=assistant_agent_response)
        print("json_object: ", json_object)
        agent_tools.createNewScript(json_object)

        # the code below will alow the user proxy agent to run code from the newly created script

        testing_agent_response = tesing_agent.get_completion(client, str(json_object))
        print("Alexander_tester_response:", testing_agent_response)
        json_object = agent_tools.getjson(json_object_string=assistant_agent_response)
        print("Alexander_json_object: ", json_object)
        test_script = agent_tools.createNewScript(json_object)

        test_script_output = agent_tools.run_scripts(json_object=test_script.get("filename"))
        print("test_script_output: ", test_script_output)
        quit()
        # the below code is for checking the output of the newly created script and checking if it works as intented.
        completion_object = {
            "new_code_output": test_script_output,
            "assistant_response": json_object,
        }
        user_proxy_response = proxy_agent_naeblis.get_completion(client, str(completion_object))
        user_proxy_response = agent_tools.getjson(json_object_string=user_proxy_response)
        print("Naeblis_user_proxy: ", user_proxy_response)

        if user_proxy_response.get("completed"):
            print("Task is complete.")
            return user_proxy_response

        user_proxy_response = str(user_proxy_response)


if __name__ == "__main__":
    while True:
        response = runGPT(input("Enter Task Instructions: "))
        print(response.get("message_to_user"))
