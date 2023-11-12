from openai import OpenAI
import toml

openai = toml.load("../config.toml")["openai"]
client = OpenAI(organization=openai["organization"], api_key=openai["api_key"])


def getCompletion(messages):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    my_assistant = client.beta.assistants.retrieve(openai["naeblis"])
    print(my_assistant)
