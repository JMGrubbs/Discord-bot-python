from fastapi import APIRouter

homeRoutes = APIRouter()


@homeRoutes.get("/", tags=["home"], response_model=dict)
async def home():
    return {"Hello": "world"}
