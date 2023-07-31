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
        if message.author == self.user:
            return
        print(f"message from {message.author}: {message.content}")
        channel = message.channel

        # Regular expression to extract strings up to the fourth slash
        # https://stackoverflow.com/questions/73440592/typeerror-expected-token-to-be-a-str-received-class-nonetype-instead
        status_regex = re.compile('(?:.+?/){4}', re.DOTALL)
        compiled_status = re.findall(status_regex, message.content)

        if 'https://twitter.com/' in message.content and '/status' in str(compiled_status) and not message.embeds or message.embeds[0].video and 'twitter' in message.embeds[0].url:
            # Regular expression to extract URLs
            # https://macxima.medium.com/python-extracting-urls-from-strings-21dc82e2142b
            
            link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
            links = re.findall(link_regex, message.content)
            filter_links = ''
            filter_nonlinks = message.content
            
            for link in links:
                if '/status/' in link[0]:
                    filter_links += (f'{link[0][0:8]}vx{link[0][8:]} ')
                    filter_nonlinks = filter_nonlinks.replace(link[0], '')

            filter_nonlinks = filter_nonlinks.strip()
            await channel.send(content=f'From: <@{message.author.id}> {filter_nonlinks} {filter_links}')
            await message.delete()

if __name__ == "__main__":
    bot = Bot(intents=intents)
    bot.run(token=TOKEN)