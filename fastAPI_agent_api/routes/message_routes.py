from fastapi import APIRouter, HTTPException, Request

from env import API_KEY

messageRoutes = APIRouter()


async def get_api_key(api_key: str):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=400, detail="Invalid API Key")


@messageRoutes.get("/get", tags=["messages"])
async def get_messages(request: Request):
    await get_api_key(request.headers["api-key"])
    # json_messages = [
    #     message.model_dump() for message in proxy_agent.messages
    # ]
    # print(json_messages)
    return {"data": ["messages"]}


@messageRoutes.get("/sendmessage", tags=["messages"])
async def send_message(request: Request):
    await get_api_key(request.headers["api-key"])

    return {"response": {"temp": "Message sent successfully"}}
