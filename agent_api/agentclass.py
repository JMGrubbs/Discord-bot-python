import time
from pydantic import BaseModel


class Agents(BaseModel):
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

    def __pydantic_fields_set__(self, agentID, model, instructions, agentName):
        self.agentID = agentID
        self.model = model
        self.instructions = instructions
        self.agentName = agentName

    def getAgentID(self):
        return self.agentID

    # ----------------------- Thread Functions -----------------------
    def getCurrentThread(self):
        return self.currentThread

    def createNewThread(self, client):
        return client.beta.threads.create().id

    # ----------------------- Prompt Functions -----------------------
    def createNewMessage(self, client):
        return client.beta.threads.messages.create(
            thread_id=self.currentThread,
            role="user",
            content=self.currentPrompt,
        )

    def getMostRecentResponse(self, client):
        return (
            client.beta.threads.messages.list(thread_id=self.currentThread)
            .data[0]
            .content[0]
            .text.value
        )

    def retrieveRun(self, client):
        return client.beta.threads.runs.retrieve(
            thread_id=self.currentThread,
            run_id=self.currentRunId,
        )

    # ----------------------- Run Functions -----------------------
    def createNewRun(self, client):
        return client.beta.threads.runs.create(
            thread_id=self.currentThread,
            assistant_id=self.agentID,
            model=self.model,
            instructions=self.instructions,
        )

    def getRun(self, client):
        return client.beta.threads.runs.retrieve(
            thread_id=self.currentThread,
            run_id=self.currentRunId,
        )

    def cancelRun(self, client):
        return client.beta.threads.runs.cancel(
            thread_id=self.currentThread,
            run_id=self.currentRunId,
        )

    # ----------------------- Action Functions -----------------------
    def get_completion(self, client, input_message, newThread=False):
        self.currentPrompt = input_message.lower()
        if self.currentThread is None or newThread is True:
            self.currentThread = self.createNewThread(client)

        self.currentMessage = self.createNewMessage(client)

        self.currentRunId = self.createNewRun(client).id

        tries = 0
        self.runstatus = None
        while self.runstatus != "completed" and self.runstatus != "failed":
            self.runstatus = self.retrieveRun(client).status
            print(f"{self.agentName} run status: ", self.runstatus)
            if tries > 10:
                print("Error: GPT run took too long.")
                cancelRun = self.cancelRun(client)
                print("Canceled run: ", cancelRun.status)
                break
            tries += 1
            time.sleep(3)
        self.currentPromptResponse = self.getMostRecentResponse(client)

        return self.currentPromptResponse
