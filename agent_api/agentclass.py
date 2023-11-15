from openai import OpenAI
import time
import toml


class Agents:
    def __init__(self, assistant_id) -> None:
        self.gpt_assistant_id = assistant_id
        self.gpt_current_thread = None
        self.gpt_latest_input_prompt = None
        self.gpt_latest_prompt_response = None
        self.gpt_run = None

        self.gpt_api_key = toml.load("api_config.toml")["openai"]["api_key"]
        self.gpt_client = OpenAI(
            api_key=self.gpt_api_key,
        )

    # Thread functions -----------------------------
    # This function creates a new thread using the openAI API
    def create_gpt_thread(self):
        self.gpt_current_thread = self.gpt_client.beta.threads.create()

    # This function gets the current thread
    def get_thread(self):
        if self.current_thread is None:
            self.current_thread = self.create_gpt_thread()
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

    # Prompt functions ----------------------------
    # This function creates a new prompt and adds it to the current thread
    def create_gpt_prompt(self, input_message):
        self.gpt_latest_input_prompt = self.gpt_client.beta.threads.messages.create(
            thread_id=self.gpt_current_thread.id,
            role="user",
            content=input_message,
        )

    # This function gets the newest input prompt added to the thread
    def get_gpt_latest_prompt(self):
        if self.gpt_latest_input_prompt is None:
            return "Ask a question."
        return self.gpt_latest_input_prompt

    # Run functions ----------------------------
    # This function runs the current thread after a message has been created and added to the thread
    def create_gpt_run(self):
        self.gpt_run = self.gpt_client.beta.threads.runs.create(
            thread_id=self.gpt_current_thread.id,
            assistant_id=self.gpt_assistant_id,
            instructions=["Adhear to the given instructions."],
        )

    # This function gets the latest run from the current thread
    def run_gpt_prompt(self):
        # if self.gpt_run is None:
        self.gpt_run = self.create_gpt_run()

        completed = False
        while completed is False:
            run_status = self.gpt_client.beta.threads.runs.retrieve(
                thread_id=self.gpt_current_thread.id, run_id=self.gpt_run.id
            )
            if run_status.status == "completed":
                completed = True
            time.sleep(1)  # sleep to avoid hitting the API too frequently

    # Response functions ----------------------------
    # This function gets the latest response from chatGPT agent in the current thread
    def get_gpt_latest_response(self):
        return self.gpt_latest_prompt_response

    def set_gpt_latest_response(self):
        self.gpt_latest_prompt_response = (
            self.gpt_client.beta.threads.messages.list(thread_id=self.gpt_current_thread.id)
            .data[0]
            .content[0]
            .text.value
        )

    # Operational functions ----------------------------
    # The funtion runs the entire process of creating a new thread, adding a message to the thread, running the thread, and returning the response
    def run_gpt(self, input_message):
        print(input_message)
        self.create_gpt_prompt(input_message)
        self.get_gpt_latest_prompt(input_message)
        self.run_gpt_prompt()
        self.set_gpt_latest_response()
        return self.get_gpt_latest_response()
