from openai import OpenAI
import AgentClass
import AgentToolsClass
from env import api_config
from AgentDesc.ProxyAgent import proxy_agent
from AgentDesc.AssistantAgent import assistant_agent

# from AgentDesc.TestingAgent import testing_agent

OPENAI_API_KEY = api_config["openai"]["api_key"]
client = client = OpenAI(
    api_key=OPENAI_API_KEY,
)

# runtime setup
model = "gpt-3.5-turbo-1106"

proxy_agent_naeblis = AgentClass.Agents(
    agentName=proxy_agent.get("proxy_agent").get("name"),
    instructions=proxy_agent.get("proxy_agent").get("metadata").get("instructions"),
    agentID=proxy_agent.get("proxy_agent").get("assistant_id"),
    model=model,
)

assistant_agent = AgentClass.Agents(
    agentName=assistant_agent.get("assistant_agent").get("name"),
    instructions=assistant_agent.get("assistant_agent").get("metadata").get("instructions"),
    agentID=assistant_agent.get("assistant_agent").get("assistant_id"),
    model=model,
)

# tesing_agent = AgentClass.Agents(
#     agentName=agents.get("testing_agents").get("name"),
#     instructions=agents.get("testing_agents").get("metadata").get("instructions"),
#     agentID=agents.get("testing_agents").get("assistant_id"),
#     model=model,
# )

agent_tools = AgentToolsClass.AgentTools(
    workspace="tools/agent_workspace/", tools="tools/agent_tools/"
)

messages = []


def runGPT(input_message):
    input_message = input_message.lower()
    if input_message == "exit":
        print("Goodbye.")
        quit()

    user_proxy_response = proxy_agent_naeblis.get_completion(client, input_message)
    print("Naeblis_user_proxy: ", user_proxy_response)
    running = True
    while running:
        print("Working...")
        # the below code is gets coding assistants response to the user proxy agents prompt
        assistant_agent_response = assistant_agent.get_completion(client, user_proxy_response)
        print("Kirk_assistant_response:", assistant_agent_response)

        # the below code is for creating a new script from the coding assistants response
        json_object = agent_tools.getjson(json_object_string=assistant_agent_response)
        print("json_object: ", json_object)
        agent_tools.createNewScript(json_object)

        test_script_output = agent_tools.run_scripts(filename=json_object.get("filename"))
        print("test_script_output: ", test_script_output)
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
            running = False

        user_proxy_response = str(user_proxy_response)

    print(user_proxy_response)
    runGPT(input("Enter Task Instructions: "))


if __name__ == "__main__":
    response = runGPT(input("Enter Task Instructions: "))
