import time

# from pydantic import BaseModel
# import asyncio
from openai import OpenAI
from env import api_config

OPENAI_API_KEY = api_config["openai"]["api_key"]
CLIENT = OpenAI(
    api_key=OPENAI_API_KEY,
)


class Agents:
    agentName: str
    agentID: str
    model: str
    instructions: str
    currentThread: str = None
    currentMessage: str = None
    currentPrompt: str = None
    currentPromptResponse: str = None
    currentRunId: str = None
    runstatus: str = None
    network_messages: list[dict] = []

    def __init__(self, agentID, model, instructions, agentName):
        self.agentID = agentID
        self.model = model
        self.instructions = instructions
        self.agentName = agentName
        self.network_messages = []

    def getAgentID(self):
        return self.agentID

    # ----------------------- Thread Functions -----------------------
    def getCurrentThread(self):
        return self.currentThread

    def createNewThread(self):
        print(CLIENT)
        return CLIENT.beta.threads.create().id

    # ----------------------- Prompt Functions -----------------------
    def createNewMessage(self):
        return CLIENT.beta.threads.messages.create(
            thread_id=self.currentThread,
            role="user",
            content=self.currentPrompt,
        )

    def getResponseFromOpenai(self):
        return CLIENT.beta.threads.messages.list(thread_id=self.currentThread).data[0].content[0].text.value

    def getCurrentPromptResponse(self):
        if self.currentPromptResponse is None:
            return {"error": "No prompt response."}
        return self.currentPromptResponse

    def clearCurrentPromptResponse(self):
        self.currentPromptResponse = None

    def retrieveRun(self):
        return CLIENT.beta.threads.runs.retrieve(
            thread_id=self.currentThread,
            run_id=self.currentRunId,
        )

    def getNetworkMessages(self):
        return self.network_messages

    def setNetworkMessages(self, message):
        network_message = {
            "agent": self.agentName,
            "task": "get_completion",
            "message": message,
        }
        self.network_messages.append(network_message)

    # ----------------------- Run Functions -----------------------
    def createNewRun(self):
        return CLIENT.beta.threads.runs.create(
            thread_id=self.currentThread,
            assistant_id=self.agentID,
            model=self.model,
            instructions=self.instructions,
        )

    def getRun(self):
        return CLIENT.beta.threads.runs.retrieve(
            thread_id=self.currentThread,
            run_id=self.currentRunId,
        )

    def cancelRun(self):
        return CLIENT.beta.threads.runs.cancel(
            thread_id=self.currentThread,
            run_id=self.currentRunId,
        )

    # ----------------------- Action Functions -----------------------
    async def get_completion(self, input_message, newThread=False) -> str:
        self.setNetworkMessages(input_message)

        self.runstatus = "completed"
        self.currentPromptResponse = input_message

        # return input_message

        self.currentPrompt = input_message.lower()
        result = self.currentPrompt

        if self.currentThread is None or newThread is True:
            self.currentThread = self.createNewThread()

        self.currentMessage = self.createNewMessage()

        self.currentRunId = self.createNewRun().id

        tries = 0
        self.runstatus = None
        while self.runstatus != "completed" and self.runstatus != "failed":
            self.runstatus = self.retrieveRun().status
            print(f"{self.agentName} run status: ", self.runstatus)
            if tries > 10:
                cancelRun = self.cancelRun()
                return {"error": "GPT run took too long.", "run": cancelRun}
            tries += 1
            time.sleep(1)

        self.currentPromptResponse = self.getResponseFromOpenai()

        result = self.currentPromptResponse

        if not isinstance(result, str):
            print("Error: Expected function to return an str")
            raise TypeError("Expected function to return an str")

        return result
