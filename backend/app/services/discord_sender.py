import asyncio
import discord
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

client = discord.Client(intents=discord.Intents.default())


async def send_prompt(prompt):
    await client.wait_until_ready()

    channel = client.get_channel(CHANNEL_ID)

    if channel:
        await channel.send(f"/imagine prompt: {prompt}")


def generate_midjourney_image(prompt):

    async def runner():
        await send_prompt(prompt)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(client.start(TOKEN))