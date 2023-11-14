from openai import OpenAI
import toml
import time

assistant_id = toml.load("config.toml")["openai"]["kirk"]
api_key = toml.load("config.toml")["openai"]["api_key"]

client = OpenAI(
    api_key=api_key,
)

# thread = client.beta.threads.create()

gpt_thread_id = "thread_9Cqr5vN2lkZxiTtdMbUvGC6k"
# messageText = "Who are you?"
# message = client.beta.threads.messages.create(
#     thread_id=gpt_thread_id,
#     role="user",
#     content=messageText,
# )

# run = client.beta.threads.runs.create(
#     thread_id=gpt_thread_id,
#     assistant_id=assistant_id,
# )

# run = client.beta.threads.runs.retrieve(thread_id=gpt_thread_id, run_id=run.id)

# # to get value of a message
# # messages.data[0].content[0].text.value
# print("waiting")

# time.sleep(10)


messages = client.beta.threads.messages.list(thread_id=gpt_thread_id)


attempt = 0
message_ret = False
while not message_ret:
    if messages.data[0].assistant_id:
        print("Boom", messages.data[0].content[0].text.value)
        message_ret = True
    else:
        print("no response yet")
        if attempt > 10:
            message_ret = True
        attempt += 1
        time.sleep(3)

print(messages)
