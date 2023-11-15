from openai import OpenAI
import time


class Agents:
    def __init__(self, init_data) -> None:
        self.gpt_assistant_id = init_data["gpt_assistant_id"]
        self.converce_command = init_data["converce_command"]
        gpt_api_key = init_data["gpt_api_key"]
        self.gtp_current_thread = None
        self.gpt_client = OpenAI(
            api_key=gpt_api_key,
        )
        self.gpt_latest_message = None
        self.gpt_run = None

    # Thread functions -----------------------------
    # This function creates a new thread using the openAI API
    def create_gtp_thread(self):
        self.gtp_current_thread = self.gpt_client.beta.threads.create()

    # This function gets the current thread
    def get_thread(self):
        if self.current_thread is None:
            self.current_thread = self.create_gtp_thread()
        return self.current_thread

    # Client functions -----------------------------
    # The function creates a new client using the openAI API
    def create_new_gpt_client(self):
        self.gpt_client = OpenAI(
            api_key=self.gpt_api_key,
        )

    # This function gets the current client
    def get_gpt_client(self):
        if self.gpt_client is None:
            self.create_new_gpt_client()
            return self.gpt_client
        return self.gpt_client

    # Message functions ----------------------------
    # This function creates a new message in the current thread
    def create_gtp_message(self, p_message):
        self.gpt_latest_message = self.gpt_client.beta.threads.messages.create(
            thread_id=self.gtp_current_thread.id,
            role="user",
            content=p_message,
        )

    # This function gets the latest message from the thread
    def get_gpt_message(self, p_message):
        if self.gpt_latest_message is None:
            self.gpt_latest_message = self.create_gtp_message(p_message)
            return self.gpt_latest_message
        return self.gpt_latest_message

    # Run functions ----------------------------
    # This function runs the current thread after a message has been created and added to the thread
    def create_gtp_run(self):
        self.gpt_run = self.gpt_client.beta.threads.runs.create(
            thread_id=self.gtp_current_thread.id,
            assistant_id=self.gpt_assistant_id,
            # instructions=,
        )

    # This function gets the latest run from the current thread
    def get_gpt_run(self):
        if self.gpt_run is None:
            self.gpt_run = self.create_gtp_run()

        completed = False
        while completed is False:
            run_status = self.gpt_client.beta.threads.runs.retrieve(
                thread_id=self.gpt_current_thread.id, run_id=self.gpt_run.id
            )
            if run_status.status == "completed":
                completed = True
            time.sleep(1)  # sleep to avoid hitting the API too frequently

        return self.gpt_run
