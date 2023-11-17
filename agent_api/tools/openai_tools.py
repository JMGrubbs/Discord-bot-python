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


def create_gpt_run(client, thread_id, assistant_id):
    return client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        model="gpt-3.5-turbo-1106",
        instructions="""IInstructions:
            1. Responsed with ONLY a valid json object in the form of a string "{object}"
            2. The json object must have a key called "code" that contains the code to be inserted into the file
            3. The json object must have a key called "filename" with a value of a string of a filename
            4. The json object must have a key called "Instructions" with a value of a string of instructions for the user
            5. The python code must print "Hello world"

        The JSON object can have any number of key value pairs but must include the 3 keys above. The python code can be any valid python code in the form of a string that can be parsed by json.loads(). The filename can be any valid filename in string format. The instructions can be any valid string.
        Example response: "{"code": "print('Hello world')", "filename": "hello.py", "Instructions": "print hello world"}" """,
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


def create_file(json_object):
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
    print(string)
    return json.loads(string)


# Create me a python script that prints "Hello world" return a stringifid json object
