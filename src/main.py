import discord
import os
from dotenv import load_dotenv

load_dotenv()

INTENTS = discord.Intents.default()
INTENTS.message_content = True

CLIENT = discord.Bot(intents=INTENTS)


@CLIENT.event
async def on_connect():
    print(f"Connected to discord as {CLIENT.user}")
    await CLIENT.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/upscale"))

CLIENT.load_extensions("cogs")
CLIENT.run(os.getenv("BOT_TOKEN"))
