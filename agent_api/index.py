from openai import OpenAI
import classes.Agent as Agent
from datetime import datetime
import classes.AgentTools as AgentTools
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

proxy_agent_naeblis = Agent.Agents(
    agentName=proxy_agent.get("proxy_agent").get("name"),
    instructions=proxy_agent.get("proxy_agent").get("metadata").get("instructions"),
    agentID=proxy_agent.get("proxy_agent").get("assistant_id"),
    model=model,
)

assistant_agent = Agent.Agents(
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

agent_tools = AgentTools.AgentTools(workspace="tools/agent_workspace/", tools="tools/agent_tools/")

returnPackage = {
    "messages": [],
    "file": {"fileName": "TestFile", "Content": "print('Hello World')"},
}

newAgentMessage = {
    "status": "complete",
    "sender": "agent",
    "timestamp": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
    "message": "Hello, how are you?",
    "id": len(returnPackage["messages"]),
}


def addMessage(input_message) -> dict:
    new_text = input_message.lower()
    message = {
        "status": "processing",
        "sender": "user",
        "timestamp": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "message": new_text,
        "id": len(returnPackage["messages"]),
    }
    returnPackage["messages"].append(message)
    # agentResponse = createMessageResponse(input_message)
    # returnPackage["messages"].append(agentResponse)
    return {"response": returnPackage}


# def createMessageResponse(input_message) -> dict:
#     try:
#         new_text = input_message.lower()
#         message = {
#             "sender": "agent",
#             "timestamp": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
#             "message": new_text,
#             "id": len(returnPackage["messages"]),
#         }
#         return message
#     except Exception as e:
#         print(e)
#         return {"status": "error", "errMessage": e, "response": None}


def getMessages() -> dict:
    if newAgentMessage["status"] == "complete":
        returnPackage["messages"][-1]["status"] = "complete"
        returnPackage["messages"].append(newAgentMessage)
    return returnPackage


def deleteMessages() -> dict:
    returnPackage["messages"] = []
    return {"status": "complete", "response": returnPackage}
