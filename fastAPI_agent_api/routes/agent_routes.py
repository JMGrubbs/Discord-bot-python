from fastapi import APIRouter, HTTPException, Request

from agent.tools import (
    get_agents_from_openai,
    get_agents_from_cache,
    get_agent_from_cache,
    create_agent_obj,
)


from env import API_KEY

agentRoutes = APIRouter()

# class ResponseModel(BaseModel):
#     data: Union[dict, list]

proxy_agent = None


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
    await get_api_key(request.headers["api-key"])

    global proxy_agent
    proxy_agent = await create_agent_obj(request.path_params["agent_id"])

    return {"agent": proxy_agent.model_dump()}


@agentRoutes.get("/proxy/agent")
async def get_proxy_agent(request: Request):
    await get_api_key(request.headers["api-key"])

    global proxy_agent
    if proxy_agent is None:
        return {"Status": "No agent set!"}

    return proxy_agent


@agentRoutes.post("/proxy/thread/{thread_id}")
async def set_proxy_thread(request: Request):
    await get_api_key(request.headers["api-key"])

    global proxy_agent
    if proxy_agent is None:
        return {"Status": "No agent set!"}

    proxy_agent.current_thread_id = request.path_params["thread_id"]

    return proxy_agent


@agentRoutes.post("/proxy/message")
async def add_proxy_message(request: Request):
    await get_api_key(request.headers["api-key"])

    req_json = await request.json()

    global proxy_agent
    if proxy_agent is None:
        return {"Status": "No agent set!"}

    message = req_json.get("user-input")
    await proxy_agent.get_completion(message)

    return proxy_agent
