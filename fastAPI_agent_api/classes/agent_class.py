from pydantic import BaseModel
from classes.thread_class import Thread

from openai_client import openai_client_connection


class Metadata(BaseModel):
    role: str
    instructions: str


class Agent(BaseModel):
    name: str
    assistant_id: str
    working: bool
    metadata: Metadata

    def get_agent(self):
        return {
            "name": self.name,
            "assistant_id": self.assistant_id,
            "working": self.working,
            "metadata": {
                "role": self.metadata.role,
                "instructions": self.metadata.instructions,
            },
        }

    def get_client(self):
        return openai_client_connection()

    def get_instructions(self):
        return self.metadata.instructions

    def set_working_status(self, status: bool):
        self.working = status

    def create_thread(self):
        newThread = Thread(agent=self.get_agent())
        print(newThread.dict())
        # return self.get_client().beta.thread.create()
