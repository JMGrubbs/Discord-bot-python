import discord
import KirkBot.responses as responses
import toml


async def send_message(
    message, user_message, is_private=False
):  # This is the function that sends the message
    try:
        response = responses.handle_responses(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
        await message.channel.send("Something went wrong")


def run_discord_bot():
    TOKEN = toml.load("config.toml")["kirkToken"]
    intents = discord.Intents.default()  # This sets up the default intents
    intents.message_content = True  # This allows the bot to read messages
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is running and has connected to Discord!")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)  # This gets the username of the user
        user_message = message.content.lower()  # This gets the message the user sent
        channel = message.channel  # This gets the channel the message was sent in
        if str(channel) == "bot-chat":
            if user_message.startswith(
                "?"
            ):  # This checks if the message starts with a "?" and if so sends the message directly to the user
                await send_message(message, user_message[1:], is_private=True)
            elif user_message.startswith("k!"):
                await send_message(message, user_message[2:])
            elif user_message.startswith("all!"):
                await send_message(message, user_message[5:])

    client.run(TOKEN)
