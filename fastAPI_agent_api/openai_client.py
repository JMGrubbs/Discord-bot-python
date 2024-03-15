from contextlib import asynccontextmanager
from env import OPEN_AI_API_KEY
from openai import OpenAI


@asynccontextmanager
async def openai_client_connection():
    CLIENT = OpenAI(
        api_key=OPEN_AI_API_KEY,
    )
    try:
        yield CLIENT
    finally:
        await CLIENT.close()
