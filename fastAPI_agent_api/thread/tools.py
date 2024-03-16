from openai_client import openai_client_connection
from cache.tools import get_set_cache


async def create_thread():
    async with openai_client_connection() as client:
        new_thread = client.beta.threads.create()
        await get_set_cache(key=new_thread.id, namespace="threads", thread=new_thread.model_dump())
        return new_thread


async def get_thread_from_openai(thread_id):
    async with openai_client_connection() as client:
        return client.beta.threads.retrieve(thread_id).model_dump()


async def get_thread(thread_id):
    return await get_set_cache(key=thread_id, namespace="threads", callback=get_thread_from_openai)


async def get_threads():
    return await get_set_cache(key=None, namespace="threads")
