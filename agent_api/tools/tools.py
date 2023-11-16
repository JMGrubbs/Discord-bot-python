from openai_tools import create_gpt_thread, create_gpt_client, create_gpt_prompt, create_gpt_run
import toml

OPENAI_API_KEY = toml.load("api_config.toml")["openai"]["api_key"]

# Dictionary to hold multiple agents, keyed by assistant_id
agents = {
    "proxy_agent": {
        "name": "Naeblis",
        "assistant_id": toml.load("api_config.toml")["openai"]["naeblis"],
        "working": False,
        "thread": None,
        "metadata": {
            "role": "user",
            "instructions": "Instructions: You are a proxy agent. You will be given on objective by the user. You will then create detailed instructions on how to accomplish the task and give them to the assistan agents. Have a continual dialog with the assistant agents to ensure they are on the right track based on their outputs.",
            "message_prompts": [],
            "message_replies": [],
        },
    },
    "assistant_agents": [
        {
            "name": "Kirk",
            "assistant_id": toml.load("api_config.toml")["openai"]["kirk"],
            "working": False,
            "thread": None,
            "metadata": {
                "role": "user",
                "instructions": "Instructions: Create software based on instructions and specifications given by the user.",
                "message_prompts": [],
                "message_replies": [],
            },
        },
        {
            "name": "Alexander",
            "assistant_id": toml.load("api_config.toml")["openai"]["alexander"],
            "working": False,
            "thread": None,
            "metadata": {
                "role": "user",
                "instructions": "Instructions: Create software based on instructions and specifications given by the user.",
                "message_prompts": [],
                "message_replies": [],
            },
        },
    ],
}


def get_completion(input_message):
    create_gpt_client(OPENAI_API_KEY)
    proxy_agent = agents["proxy_agent"]
    proxy_agent["metadata"]["message_prompts"].append(input_message)
    proxy_agent["thread"] = create_gpt_thread(input_message, proxy_agent)
    new_prompt = create_gpt_prompt(
        proxy_agent["thread"], input_message, proxy_agent.get("metadata")
    )
    proxy_agent["metadata"]["message_prompts"].append(new_prompt)

    proxy_agent["run"] = create_gpt_run(
        proxy_agent["thread"], proxy_agent["assistant_id"], proxy_agent.get("metadata")
    )

    return
