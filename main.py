import discord
import os
import re


# check discord version
print(discord.__version__)

# initialize dotenv
TOKEN = os.environ.get("DISCORD_TOKEN")

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

        if ('https://twitter.com/' in message.content and not message.embeds):
            # Regular expression to extract URLs
            # https://macxima.medium.com/python-extracting-urls-from-strings-21dc82e2142b
            
            link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
            links = re.findall(link_regex, message.content)
            filter_links = ''
            
            for link in links:
                filter_links += (f'{link[0][0:8]}vx{link[0][8:]} ')
                msg = message.content.split(link[0])
                msg = "".join(msg)

            await channel.send(content=f'From: <@{message.author.id}> {msg} {filter_links}')
            await message.delete()

if __name__ == "__main__":
    bot = Bot(intents=intents)
    bot.run(token=TOKEN)