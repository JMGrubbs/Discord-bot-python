import classes.Agent as Agent

# import asyncio


class Operations:
    response: dict = {}
    proxy_agent: Agent = None
    proxy_agent_messages: list[dict] = []
    assistant_agent: Agent = None
    assistant_agent_messages: list[dict] = []

    newUserMessage: dict = None
    newAgentMessage: dict = None

    def __init__(self, proxy_agent, assistant_agent):
        self.proxy_agent = proxy_agent
        self.assistant_agent = assistant_agent

        self.response = {
            "messages": [],
            "file": {
                "fileName": "TestFile",
                "Content": "print('Hello World')",
            },
            "network_box": {
                "proxy_network_messages": [],
                "assistant_network_messages": [],
            },
        }

    def createMessage(self, input_message, author) -> dict:
        message = {
            "sender": author,
            "id": len(self.response["messages"]) + 1,
        }
        if author == "user":
            message["status"] = "complete"
            message["message"] = input_message
        elif author == "agent":
            message["status"] = "processing"
            message["message"] = None

        self.response["messages"].append(message)

    async def addMessage(self, data) -> dict:
        new_message = data["message"].lower()

        # Create a new message object for the incoming message from the user
        self.createMessage(new_message, data.get("sender"))
        # Create a new message object for the agents response to the user
        self.createMessage(new_message, "agent")

        completion = await self.proxy_agent.get_completion(new_message)

        self.response["messages"][-1]["message"] = completion
        self.response["messages"][-1]["status"] = "complete"

    def getResponse(self) -> dict:
        self.response["proxy_network_messages"] = self.proxy_agent.getNetworkMessages()
        return {"response": self.response}

    def clearMessages(self):
        self.response["messages"] = []
        return {"response": self.response}
