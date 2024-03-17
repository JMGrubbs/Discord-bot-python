from pydantic import BaseModel
from typing import Optional, List
import time

from openai_client import openai_client_connection

INSTRUCTIONS = (
    """Your job is to answer questions in an informative and cordial way.""",
)


class Agent(BaseModel):
    id: str
    created_at: int
    description: Optional[str]
    file_ids: list
    instructions: str
    metadata: Optional[dict]
    model: str
    name: str
    object: str
    tools: List[dict]

    current_thread_id: Optional[str] = None
    current_run_status: Optional[str] = None
    messages: list = []

    async def get_completion(self, prompt: str):
        async with openai_client_connection() as client:
            new_user_prompt = client.beta.threads.messages.create(
                thread_id=self.current_thread_id,
                content=prompt,
                role="user",
            )
            self.messages.append(new_user_prompt.model_dump())
            new_run = client.beta.threads.runs.create(
                thread_id=self.current_thread_id,
                assistant_id=self.id,
                # instructions=self.instructions,
                instructions=INSTRUCTIONS[0],
            )
            self.current_run_status = new_run.status
            while self.current_run_status != "completed":
                new_run = client.beta.threads.runs.retrieve(
                    thread_id=self.current_thread_id, run_id=new_run.id
                )
                self.current_run_status = new_run.status
                time.sleep(0.5)

            completion = client.beta.threads.messages.list(
                thread_id=self.current_thread_id
            ).data

            self.messages.append(completion)

    async def fetch_messages(self):
        async with openai_client_connection() as client:
            messages = client.beta.threads.messages.list(
                thread_id=self.current_thread_id
            ).data
            self.messages = messages
