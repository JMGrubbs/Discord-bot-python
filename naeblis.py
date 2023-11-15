# from openai import OpenAI
import toml
import NaeblisBot.bot as NaeblisBot
from agent_class.agentclass import Agents

assistant_id = toml.load("config.toml")["openai"]["naeblis"]
gpt_api_key = toml.load("config.toml")["openai"]["api_key"]

init_data = {
    "gpt_assistant_id": assistant_id,
    "converce_command": "/naeblis",
    "gpt_api_key": gpt_api_key,
}

if __name__ == "__main__":  # This is the main function
    naeblis = Agents(init_data)
    NaeblisBot.run_discord_bot()
    pass
