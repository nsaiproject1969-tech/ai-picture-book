import discord
import os
import asyncio

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def generate_midjourney_image(prompt):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(send_midjourney_prompt(prompt))

    return "Image request sent to Midjourney"

async def send_midjourney_prompt(prompt):

    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        print("Channel not found")
        return

    await channel.send(f"/imagine prompt: {prompt}")


@client.event
async def on_ready():
    print(f"Bot connected as {client.user}")

    channel = client.get_channel(CHANNEL_ID)

    if channel:
        await channel.send("AI Picture Book Bot is online 🚀")

        await send_midjourney_prompt(
            "children book illustration of a brave mouse exploring a forest"
        )




if __name__ == "__main__":
    client.run(TOKEN)
