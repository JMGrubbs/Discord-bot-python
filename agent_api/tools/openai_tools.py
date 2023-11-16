from openai import OpenAI

client = None


def create_gpt_client(api_key):
    global client
    client = OpenAI(
        api_key=api_key,
    )
    return client


def create_gpt_thread(client):
    return client.beta.threads.create()


def create_gpt_prompt(thread, input_message, metadata):
    return client.beta.threads.messages.create(
        thread_id=thread,
        role=metadata.get("role"),
        content=input_message,
    )


def create_gpt_run(thread, assistant_id, metadata):
    return client.beta.threads.runs.create(
        thread_id=thread,
        assistant_id=assistant_id,
        instructions=metadata.get("instructions"),
    )
