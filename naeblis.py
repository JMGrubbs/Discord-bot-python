# from openai import OpenAI
# import toml
import NaeblisBot.bot as NaeblisBot

# assistant_id = toml.load("config.toml")["openai"]["naeblis"]
# api_key = toml.load("config.toml")["openai"]["api_key"]

# client = OpenAI(
#     api_key=api_key,
# )

# thread_id = "thread_Dmn8WoXCALWDlHViLpifScCc"
# run_id = "run_kgCd6q9lE9hvTloTwWsHjHxB"

if __name__ == "__main__":  # This is the main function
    NaeblisBot.run_discord_bot()
    pass
