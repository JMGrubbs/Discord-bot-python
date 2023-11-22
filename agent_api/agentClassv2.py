from pydantic import BaseModel


class Agents(BaseModel):
    agentName: str
    agentID: str
    model: str
    instructions: str
    currentThread: str = None
    currentMessage: str = None
    currentPrompt: str = None
    currentRunId: str = None

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
        self.currentThread = client.beta.threads.create().id
        return self.currentThread

    # ----------------------- Prompt Functions -----------------------
    def createNewMessage(self, client):
        self.currentMessage = client.beta.threads.messages.create(
            thread_id=self.currentThread,
            role="user",
            content=self.currentPrompt,
        )
        return self.currentMessage

    def getMostRecentResponse(self, client):
        return (
            client.beta.threads.messages.list(thread_id=self.currentThread)
            .data[0]
            .content[0]
            .text.value
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

    def get_completion(self, client, input_message):
        self.currentPrompt = input_message
        self.createNewMessage(client)

        quit()
        self.currentRunId = self.createNewRun(client).id
        self.run_gpt_prompt()
        self.set_gpt_latest_response()
        return self.get_gpt_latest_response()
