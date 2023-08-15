import discord
import os
import re


# check discord version
print(discord.__version__)

# initialize dotenv
# production env
TOKEN = os.environ.get("DISCORD_TOKEN")

# local env loading
# from dotenv import load_dotenv
# load_dotenv()
# TOKEN = os.getenv("DISCORD_TOKEN")

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

        if ('https://twitter.com/' in message.content or 'https://x.com/' in message.content) and '/status' in str(compiled_status):
            # Regular expression to extract URLs
            # https://macxima.medium.com/python-extracting-urls-from-strings-21dc82e2142b
            
            link_regex = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
            links = re.findall(link_regex, message.content)
            filter_links = ''
            filter_nonlinks = message.content
            
            for link in links:
                original_link = link[0]
                compressed_link = link[0]
                if 'https://x.com/' in compressed_link:
                    compressed_link = f'{compressed_link[0:8]}twitter{compressed_link[9:]}'
                if '/status/' in compressed_link:
                    filter_links += (f'{compressed_link[0:8]}vx{compressed_link[8:]} ')
                    filter_nonlinks = filter_nonlinks.replace(original_link, '')

            filter_nonlinks = filter_nonlinks.strip()

            await channel.send(content=f'From: <@{message.author.id}> {filter_nonlinks} {filter_links}')
            await message.delete()

if __name__ == "__main__":
    bot = Bot(intents=intents)
    bot.run(token=TOKEN)