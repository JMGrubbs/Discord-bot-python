from openai_client import openai_client_connection
from cache.tools import get_set_cache
from agent.agent_class import Agent


async def get_agents_from_openai():
    agents = []
    async with openai_client_connection() as client:
        agents = client.beta.assistants.list()
        agents = [{agent.model_dump().get("id"): agent.model_dump()} for agent in agents]

    for agent in agents:
        agent_id = list(agent.keys())[0]
        await get_set_cache(key=agent_id, namespace="agents", obj_type=agent)
    return agents


async def get_agents_from_cache():
    return await get_set_cache(namespace="agents")


async def create_agent_obj(agent_id):
    agent_json = await get_agent_from_cache(agent_id)
    new_agent_obj = Agent(**agent_json)
    return new_agent_obj


async def get_agent_from_cache(agent_id):
    return await get_set_cache(key=agent_id, namespace="agents")
