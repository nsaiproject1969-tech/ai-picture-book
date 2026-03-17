import discord
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot connected as {client.user}")

    channel = client.get_channel(CHANNEL_ID)

    if channel:
        await channel.send("AI Picture Book Bot Test 🚀")

        await channel.send("/imagine prompt: cute mouse in forest children book illustration")

    await client.close()

client.run(TOKEN)