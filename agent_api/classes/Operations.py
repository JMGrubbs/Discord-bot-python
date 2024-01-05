import classes.Agent as Agent


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
            message["message"] = "Hello World"

        self.response["messages"].append(message)

    def addMessage(self, data) -> dict:
        new_message = data["message"].lower()
        # Create a new message object for the incoming message from the user, and add it to the messages list
        self.createMessage(new_message, data.get("sender"))
        self.createMessage(new_message, "agent")

        return {"response": self.response}

    def getResponse(self) -> dict:
        if self.response["messages"][-1]["status"] == "processing":
            self.response["messages"][-1]["status"] = "complete"
            return {"response": self.response}
        return {"response": self.response}

    def clearMessages(self):
        self.response["messages"] = []
        return {"response": self.response}


# async def my_async_function():
#     print("Start of async function")
#     await asyncio.sleep(1)  # Simulating an async IO operation
#     print("End of async function")

# # Running the async function
# async def main():
#     await my_async_function()

# asyncio.run(Opperations.addMessage())
