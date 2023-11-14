from openai import OpenAI
import toml
import time

assistant_id = toml.load("config.toml")["openai"]["alexander"]
api_key = toml.load("config.toml")["openai"]["api_key"]
gtp_thread_id = toml.load("config.toml")["openai"]["alexanderThread"]

client = OpenAI(
    api_key=api_key,
)


def handle_responses(message):
    p_message = message
    if p_message == "!stop":
        quit()
    try:
        message = client.beta.threads.messages.create(
            thread_id=gtp_thread_id,
            role="user",
            content=p_message,
        )

        run = client.beta.threads.runs.create(
            thread_id=gtp_thread_id,
            assistant_id=assistant_id,
            instructions="You are discusising the Borg invation with Captain Kirk. The user has a premium account.",
        )

        completed = False
        while completed is False:
            run_status = client.beta.threads.runs.retrieve(thread_id=gtp_thread_id, run_id=run.id)
            if run_status.status == "completed":
                completed = True
            time.sleep(1)  # sleep to avoid hitting the API too frequently

        messages = client.beta.threads.messages.list(thread_id=gtp_thread_id)
        return "k! " + str(messages.data[0].content[0].text.value)
    except Exception as e:
        print(e)
        return "Something went wrong"
