from openai import OpenAI
import toml
import time

assistant_id = toml.load("config.toml")["openai"]["naeblis"]
api_key = toml.load("config.toml")["openai"]["api_key"]

# gtp_thread_id = toml.load("config.toml")["openai"]["naeblisThread"]


client = OpenAI(
    api_key=api_key,
)


def create_thread():
    try:
        thread = client.beta.threads.create()
        return thread
    except Exception as e:
        print(e)
        return False


def handle_responses(message, gpt_current_thread):
    p_message = message
    if p_message == "!stop":
        quit()
    try:
        message = client.beta.threads.messages.create(
            thread_id=gpt_current_thread.id,
            role="user",
            content=p_message,
        )

        run = client.beta.threads.runs.create(
            thread_id=gpt_current_thread.id,
            assistant_id=assistant_id,
            instructions="Continue evolving the Borg invasion based on the respones of Captain Kirk and Alexander the Great.",
        )

        completed = False
        while completed is False:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=gpt_current_thread.id, run_id=run.id
            )
            if run_status.status == "completed":
                completed = True
            time.sleep(1)  # sleep to avoid hitting the API too frequently

        messages = client.beta.threads.messages.list(thread_id=gpt_current_thread.id)
        return "/all " + str(messages.data[0].content[0].text.value)
    except Exception as e:
        print(e)
        return "Something went wrong"
