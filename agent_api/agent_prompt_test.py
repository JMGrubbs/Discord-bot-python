from openai import OpenAI
import AgentClass
import toml

OPENAI_API_KEY = toml.load("api_config.toml")["openai"]["api_key"]
client = client = OpenAI(
    api_key=OPENAI_API_KEY,
)
agents = {
    "testing_agents": {
        "name": "Alexander",
        "assistant_id": toml.load("api_config.toml")["openai"]["alexander"],
        "metadata": {
            "role": "user",
            "instructions": """
                You are a code testing agent. When called you need to write a test for the code that the assistant agent creates.
                As a top-tier programming AI, you are adept at creating accurate Python scripts. You will properly name files and craft precise Python code with the appropriate imports to fulfill the user's request. Ensure to execute the necessary code before responding to the user.

                You are a code-testing agent. When called you need to write and return a python script that tests the code that the assistant agent created.
                Instructions:
                    1. Create a test script for the python script created by the agent using the file name from the assistant.
                    2. Import the script and the function from the script that the assistant created.
                    3. You will be given a the script in the form of a string
                    4. Return the output of the test in the form of a json object with the following keys: "testCode" as a string
                    5. Responed with only a json object
            """,
        },
    },
}
model = "gpt-3.5-turbo-1106"

tesing_agent = AgentClass.Agents(
    agentName=agents.get("testing_agents").get("name"),
    instructions=agents.get("testing_agents").get("metadata").get("instructions"),
    agentID=agents.get("testing_agents").get("assistant_id"),
    model=model,
)

prompt = {
    "code": "from datetime import datetime\n\ndef get_current_datetime():\n    return datetime.now()",
    "filename": "date_utils.py",
    "Instructions": "This Python script defines a function called get_current_datetime, which returns the current datetime when called.",
}

response = tesing_agent.get_completion(client=client, input_message=str(prompt))

print(response)
