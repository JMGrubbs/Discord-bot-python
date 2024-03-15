from env import api_config

model = "gpt-3.5-turbo-1106"

assistant_agent = {
    "assistant_agent": {
        "name": "Kirk",
        "assistant_id": api_config["openai"]["kirk"],
        "metadata": {
            "role": "user",
            "instructions": """
                    Instructions:
                        1. Your response must be in the form of a json object
                        2. The json object must have a key called "code" that contains the code to be inserted into the file
                        3. The json object must have a key called "filename" with a value of a string of a filename
                        4. The json object must have a key called "Instructions" with a value of a string of instructions for the user

                    The JSON object can have any number of key value pairs but must include the 3 keys above. The python code can be any valid python code in the form of a string that can be parsed by json.loads(). The filename can be any valid filename in string format. The instructions can be any valid string.
                    Example response: "{"code": "print('Hello world')", "filename": "hello.py", "Instructions": "print hello world"}"
                """,
        },
    },
}
