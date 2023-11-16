# from typing import List
# from pydantic import Field
# from instructor import OpenAISchema
# import subprocess
import os


def create_gpt_thread(client):
    return client.beta.threads.create()


def create_gpt_prompt(client, thread_id, input_message):
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=input_message,
    )


def create_gpt_run(client, thread_id, assistant_id):
    return client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="""Responsed with ONLY a valid json object in this form:
        {"code": "the code in the file", "filename": "{a file name that you generate}.py", "Instructions": "a string of instructions for the user"}""",
    )


def retrieve_gpt_run(client, thread_id, run_id):
    return client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )


def get_gpt_prompt_response(client, thread_id):
    return client.beta.threads.messages.list(thread_id=thread_id).data[0].content[0].text.value


# def create_file(file_name, body, directory):
#     # Combine the directory and file name to form the full path
#     full_path = os.path.join(directory, file_name)

#     # Use the full path to open the file
#     with open(full_path, "w") as f:
#         f.write(body)

#     return "File written to " + file_name
