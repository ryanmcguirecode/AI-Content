from chatgpt_wrapper import ChatGPT
import os

def generate(prompt: str, filepath: str):
    bot = ChatGPT()
    response = bot.ask(prompt)
    with open(filepath, "w") as f:
        f.write(response.strip())
    return response