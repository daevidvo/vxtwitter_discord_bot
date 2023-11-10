import discord
import os
import re
import time
import math


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
    # prviate variables
    __nateTimer = False

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

        # for vxtwitter link automation
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

            # for replying to messages
            if message.reference:
                try:
                    msg = await self.get_channel(message.reference.channel_id).fetch_message(message.reference.message_id)

                    # holy there's so much repeated code we needa refactor sometime 💀
                    return await msg.reply(content=f'From: <@{message.author.id}> {filter_nonlinks} {filter_links}', silent=True)
                except:
                    return await channel.send(content=f'error sending reply message with twitter links') 

            # for spoiler messages
            if "||" in message.content:
                try:
                    await channel.send(content=f'@silent From: <@{message.author.id}> || {filter_nonlinks} {filter_links} ||')
                    return await message.delete()
                except:
                    return await channel.send(content=f'error sending fixed twitter link')
            try:
                await channel.send(content=f'@silent From: <@{message.author.id}> {filter_nonlinks} {filter_links}')
                return await message.delete()
            except:
                return await channel.send(content=f'error sending fixed twitter link')
       
        if message.content.startswith("!natepasta"):
            try:
                await channel.send(content=f'The truth about Nate: He is a big fat meanie, he likes to suck smelly peepee and, he makes everywhere he goes to Hell. His anger problems need to chill. He is also a domekano enjoyer 💀')
            except:
                await channel.send(content=f'error sending nate copypasta')

    async def on_raw_reaction_add(self, payload):
        msg = await self.get_channel(payload.channel_id).fetch_message(payload.message_id)

        if msg.author == self.user:
            msgAuthorID = int(msg.content.split(" ")[1][2:-1])

            if msgAuthorID == payload.user_id and str(payload.emoji) == "❌":
                await msg.delete()
                

if __name__ == "__main__":
    bot = Bot(intents=intents)
    bot.run(token=TOKEN)