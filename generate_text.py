from chatgpt_wrapper import ChatGPT
import os

def generate(prompt: str, filepath: str):
    """ Generate ChatGPT response based on prompt, save to filepath """
    
    bot = ChatGPT()
    response = bot.ask(prompt)
    with open(filepath, "w") as f:
        f.write(response.strip().replace("\"", ""))
    return response