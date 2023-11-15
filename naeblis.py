# from openai import OpenAI
import toml
import NaeblisBot.bot as NaeblisBot

assistant_id = toml.load("config.toml")["openai"]["naeblis"]

init_data = {
    "gpt_assistant_id": assistant_id,
    "converce_command": "/naeblis",  # Dynamically set as needed
    "agent_api_key": toml.load("config.toml")["agent_api"]["api_key"],
}

if __name__ == "__main__":
    NaeblisBot.run_discord_bot(init_data)
    pass
