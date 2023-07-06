import discord
import os
from dotenv import load_dotenv


load_dotenv()

class Bot: 
    def __init__(self):
        self.token = os.getenv("DISCORD_TOKEN")
        self.server = os.getenv("DISCORD_SERVER")
        pass

    def run(self):
        pass

if __name__ == "__main__":
    bot = Bot()
    bot.run()