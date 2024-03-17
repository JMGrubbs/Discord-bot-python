from fastapi import APIRouter, HTTPException, Request

from agent.tools import (
    get_agents_from_openai,
    get_agents_from_cache,
    get_agent_from_cache,
    create_agent_obj,
)
from env import API_KEY

proxy_agent = None

agentRoutes = APIRouter()

# class ResponseModel(BaseModel):
#     data: Union[dict, list]


async def get_api_key(api_key: str):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=400, detail="Invalid API Key")


@agentRoutes.get("/get/openai/agents")
async def get_agents_openai(request: Request):
    await get_api_key(request.headers["api-key"])
    agents = await get_agents_from_openai()
    return agents


@agentRoutes.get("/get")
async def get_agents(request: Request):
    await get_api_key(request.headers["api-key"])
    agents = await get_agents_from_cache()
    return agents


@agentRoutes.get("/get/agent/{agent_id}")
async def get_agent_object_from_cache(request: Request):
    await get_api_key(request.headers["api-key"])
    assistent_id = request.path_params["agent_id"]
    agent = await get_agent_from_cache(assistent_id)
    return {"agent": agent}


@agentRoutes.post("/proxy/agent/{agent_id}")
async def set_proxy_agent(request: Request):
    # await get_api_key(request.headers["api-key"])

    global proxy_agent

    new_agent_id = request.path_params["agent_id"]
    if not proxy_agent or new_agent_id != proxy_agent.id:
        proxy_agent = await create_agent_obj(
            request.path_params["agent_id"]
        )

    return {"agent": proxy_agent.model_dump()}


@agentRoutes.get("/proxy/agent")
async def get_proxy_agent(request: Request):
    await get_api_key(request.headers["api-key"])

    global proxy_agent
    if proxy_agent is None:
        return {"Status": False}

    return proxy_agent


@agentRoutes.post("/proxy/thread/{thread_id}")
async def set_proxy_thread(request: Request):
    await get_api_key(request.headers["api-key"])

    global proxy_agent
    if proxy_agent is None:
        return {"Status": False}

    proxy_agent.current_thread_id = request.path_params["thread_id"]
    await proxy_agent.fetch_messages()

    return proxy_agent


@agentRoutes.get("/proxy/messages")
async def add_proxy_message(request: Request):
    await get_api_key(request.headers["api-key"])

    global proxy_agent
    if proxy_agent is None:
        return {"Status": False}
    return {"data": proxy_agent.messages}
