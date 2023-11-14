import discord
import toml

import NaeblisBot.responses as responses


async def send_message(
    gpt_current_thread, message, user_message, is_private=False
):  # This is the function that sends the message
    try:
        response = responses.handle_responses(user_message, gpt_current_thread)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
        await message.channel.send("Something went wrong")


async def handle_create_thread(message, user_message, is_private=False):
    try:
        current_thread = responses.create_thread()
        response = "Thread creation failed"

        if current_thread:
            response = "Thread created: " + str(current_thread.id)

        await message.channel.send(response)
        return current_thread
    except Exception as e:
        print(e)
        await message.channel.send("Something went wrong")


def run_discord_bot():
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
            if user_message.startswith("/create_threads"):
                await handle_create_thread(message, user_message, is_private=False)
            if user_message.startswith("?"):
                await send_message(
                    current_thread,
                    message,
                    user_message[2:],
                    is_private=True,
                )
            elif user_message.startswith("/n"):
                await send_message(
                    current_thread,
                    message,
                    user_message[3:],
                )

    client.run(TOKEN)
