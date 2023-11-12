import random


def handle_responses(message):
    p_message = message.lower()

    if p_message == "hello":
        return "Hi"
    if p_message == "roll":
        return str(random.randint(1, 10))
    if p_message == "!help":
        return "`This message is helpful most the time`"

    print("BOOM", message)
    return "I dont know what you mean by that"
