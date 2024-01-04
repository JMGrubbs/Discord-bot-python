import classes.Agent as Agent
from datetime import datetime
import classes.AgentTools as AgentTools
from env import api_config
from AgentDesc.ProxyAgent import proxy_agent
from AgentDesc.AssistantAgent import assistant_agent

# from AgentDesc.TestingAgent import testing_agent

OPENAI_API_KEY = api_config["openai"]["api_key"]

# --------------------------------- runtime setup ---------------------------------

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

agent_tools = AgentTools.AgentTools(workspace="tools/agent_workspace/", tools="tools/agent_tools/")

returnPackage = {
    "messages": [],
    "file": {"fileName": "TestFile", "Content": "print('Hello World')"},
}

newAgentMessage = None


# --------------------------------- runtime setup ---------------------------------
# ----------------------- Route Functions -----------------------
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

    newAgentMessage = {
        "status": "processing",
        "sender": "agent",
        "timestamp": None,
        "message": None,
        "id": len(returnPackage["messages"]),
    }

    promptAgent(input_message)

    return {"response": returnPackage}


def getMessages() -> dict:
    addedMessage = setNewAgentMessage(proxy_agent_naeblis)
    if addedMessage is False:
        return {"response": returnPackage}

    returnPackage["messages"][-1]["status"] = "complete"
    returnPackage["messages"].append(newAgentMessage)
    return returnPackage


def deleteMessages() -> dict:
    returnPackage["messages"] = []
    return {"response": returnPackage}


# ----------------------- Route Functions -----------------------
# ----------------------- Helper Functions -----------------------
def setNewAgentMessage(agent) -> dict:
    currentResponse = agent.getCurrentPromptResponse()
    if currentResponse is None:
        return False

    newAgentMessage["status"] = "complete"
    newAgentMessage["timestamp"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    newAgentMessage["message"] = currentResponse
    return True


def promptAgent(input_message) -> dict:
    try:
        proxy_agent_naeblis.get_completion(input_message)
    except Exception as e:
        print(e)
        return {"status": "error", "errMessage": e, "response": None}


# ----------------------- Helper Functions -----------------------
