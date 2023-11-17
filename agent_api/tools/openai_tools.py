# from typing import List
# from pydantic import Field
# from instructor import OpenAISchema
# import subprocess
# import os
import json
import subprocess


def create_gpt_thread(client):
    return client.beta.threads.create()


def create_gpt_prompt(client, thread_id, input_message):
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=input_message,
    )


def create_gpt_run(client, thread_id, assistant):
    return client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant["assistant_id"],
        model="gpt-3.5-turbo-1106",
        instructions=assistant["metadata"]["instructions"],
    )


def retrieve_gpt_run(client, thread_id, run_id):
    return client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )


def get_gpt_prompt_response(client, thread_id):
    return client.beta.threads.messages.list(thread_id=thread_id).data[0].content[0].text.value


def cancel_gpt_run(client, thread_id, run_id):
    return client.beta.threads.runs.cancel(
        thread_id=thread_id,
        run_id=run_id,
    )


def create_run_file(json_object):
    # Define the code for the new Python script
    new_script_code = json_object.get("code")

    # Define the filename for the new Python script
    filename = json_object.get("filename")

    # Create the new Python script file with the provided code
    with open("tools/creations/" + filename, "w") as file:
        file.write(new_script_code)

    # Now, you can execute the newly created script if desired.
    # For example, you can run it using subprocess:

    result = subprocess.run(["python", filename], capture_output=True, text=True)

    # Return the output of the script
    return result.stdout


def conver_to_json(string):
    json_object = None
    Error = None
    try:
        json_object = json.loads(string[7:-3])
        return json_object
    except Exception as e:
        Error = str(("JSON ERROR: ", e))

    try:
        json_object = json.loads(string[3:-3])
        return json_object
    except Exception as e:
        Error = str(("JSON ERROR: ", e))

    try:
        json_object = json.loads(string)
        return json_object
    except Exception as e:
        Error = str(("JSON ERROR: ", e))
    return Error
