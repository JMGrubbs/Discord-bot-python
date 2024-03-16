from pydantic import BaseModel

# from typing import Optional, List


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

    def get_instructions(self):
        return self.metadata.instructions

    def set_working_status(self, status: bool):
        self.working = status
