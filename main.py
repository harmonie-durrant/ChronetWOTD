import os
import keep_alive
import discord
import asyncio
from bs4 import BeautifulSoup
import requests

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def my_background_task(self):
        await self.wait_until_ready()
        WOTD = 0
        channel = self.get_channel(865816936386527252) # channel ID goes here
        while not self.is_closed():
          page = requests.get("https://www.dictionary.com/e/word-of-the-day/")
          soup = BeautifulSoup(page.content, 'html.parser')
          WOTD = soup.find(class_="js-fit-text").text
          Pronunciation = soup.find(class_="otd-item-headword__pronunciation__text").text
          Pronunciation = Pronunciation.replace("\n", "")
          Pronunciation = Pronunciation.replace(" ", "")
          Defintion = soup.find(class_="otd-item-headword__pos").text.replace("\n", "")

          embed=discord.Embed(title="Today's WOTD is: "+WOTD, url="https://www.dictionary.com/e/word-of-the-day/", color=0xFF5733)
          embed.add_field(name="Pronunciation", value=Pronunciation, inline=False)
          embed.add_field(name="Definition", value=Defintion, inline=False)

          await channel.send(embed=embed)
          await asyncio.sleep(86400) # task runs every day


client = MyClient()
my_secret = os.environ['TOKEN']


keep_alive.keep_alive()
client.run(my_secret)
