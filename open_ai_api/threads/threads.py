from openai import OpenAI
from open_ai_api.threads.threads import ThreadFunctions

client = OpenAI()


def create_thread():
    thread = client.beta.threads.create()
    print(thread)
    ThreadFunctions.create_thread(gpt_thread_id=thread.object, metadata=thread.metadata)
    return thread


def get_thread(thread_id):
    thread = client.beta.threads.retrieve(thread_id)

    return thread


# if __name__ == "__main__":
#     thread = create_thread()
#     print(thread)
#     print(get_thread(thread))
