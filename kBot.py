import discord
from discord.ext import commands
import json


def run_bot():
    with open('config.json', 'r') as conf:
        data = json.load(conf)
        token = data["TOKEN"]

    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print(f'{client.user} is online')

    client.run(token)



