import discord
import os
from dotenv import load_dotenv


# check discord version
print(discord.__version__)

# initialize dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# set up discord
intents = discord.Intents.default()
intents.message_content = True

# creating bot
class Bot(discord.Client): 
    async def on_ready(self):
        print(f"logged on as {self.user}")

    async def on_message(self, message):
        if (message.author == self.user):
            return
        print(f"message from {message.author}: {message.content}")
        
        channel = message.channel

        await channel.send(message.content)

if __name__ == "__main__":
    bot = Bot(intents=intents)
    bot.run(token=TOKEN)