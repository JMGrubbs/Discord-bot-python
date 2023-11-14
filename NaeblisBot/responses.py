from openai import OpenAI
import toml
import time

assistant_id = toml.load("config.toml")["openai"]["naeblis"]
api_key = toml.load("config.toml")["openai"]["api_key"]

gtp_thread_id = "thread_X3n0c3tBb2TAb4EylyGJPcJG"

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
            instructions="You are discusising the Borg invation with John. The user has a premium account.",
        )

        run = client.beta.threads.runs.retrieve(thread_id=gtp_thread_id, run_id=run.id)

        time.sleep(10)

        messages = client.beta.threads.messages.list(thread_id=gtp_thread_id)

        attempt = 0
        message_ret = False
        while not message_ret:
            if messages.data[0].assistant_id:
                message_ret = True
                return messages.data[0].content[0].text.value
            else:
                if attempt > 10:
                    message_ret = True
                attempt += 1
                time.sleep(3)
        return "No response from ChatGTP API."
    except Exception as e:
        print(e)
        return "Something went wrong"
