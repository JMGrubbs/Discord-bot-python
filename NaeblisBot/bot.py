import discord
import toml

import NaeblisBot.responses as responses


# This is the function that sends the message
async def send_message(assistant_id, message, user_message, is_private=False):
    try:
        response = await responses.handle_responses(user_message, assistant_id)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
        await message.channel.send(e)


def run_discord_bot(init_data):
    assistant_id = init_data["gpt_assistant_id"]
    TOKEN = toml.load("config.toml")["discordbots"]["naeblisToken"]
    intents = discord.Intents.default()  # This sets up the default intents
    intents.message_content = True  # This allows the bot to read messages
    client = discord.Client(intents=intents)  # This sets the client up with the intents

    @client.event
    async def on_ready():
        print(f"{client.user} is running and has connected to Discord!")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        # username = str(message.author)  # This gets the username of the user
        user_message = message.content.lower()  # This gets the message the user sent
        channel = message.channel  # This gets the channel the message was sent in
        if str(channel) == "bot-chat":
            # if user_message.startswith("?"):
            #     await send_message(
            #         assistant_id,
            #         message,
            #         user_message[2:],
            #         is_private=True,
            #     )
            if user_message.startswith(init_data["converce_command"]):
                cutoff = len(init_data["converce_command"]) + 1
                await send_message(
                    assistant_id,
                    message,
                    user_message[cutoff:],
                )

    client.run(TOKEN)
