from pydantic import BaseModel
from datetime import datetime
import classes.Agent as Agent


class Opperations(BaseModel):
    response: dict = {}
    proxy_agent: Agent = None
    proxy_agent_messages: list[dict] = []
    assistant_agent: Agent = None
    assistant_agent_messages: list[dict] = []

    newUserMessage: dict = None
    newAgentMessage: dict = None

    def __pydantic_fields_set__(self, proxy_agent, assistant_agent):
        self.proxy_agent = proxy_agent
        self.assistant_agent = assistant_agent
        self.newUserMessage = None
        self.newAgentMessage = None

        self.response = {
            "messages": [],
            "file": {
                "fileName": "TestFile",
                "Content": "print('Hello World')",
            },
        }

    def createMessage(self, input_message, author) -> dict:
        message = {
            "sender": author,
            "id": len(self.messages) + 1,
        }
        if author == "user":
            message["status"] = "complete"
            message["timestamp"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            message["message"] = input_message
        elif author == "agent":
            message["status"] = "processing"
            message["timestamp"] = None
            message["message"] = None

        self.messages.append(message)

    def addMessage(self, input_message, author) -> dict:
        new_message = input_message.lower()

        # Create a new message object for the incoming message from the user, and add it to the messages list
        self.createMessage(new_message, author)

        return {"response": {"messages": self.messages, "file": self.file_object}}
