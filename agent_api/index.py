import classes.Agent as Agent
import classes.AgentTools as AgentTools
import classes.Operations as Operations
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

main_operations = Operations.Operations(
    proxy_agent=proxy_agent_naeblis, assistant_agent=assistant_agent
)
