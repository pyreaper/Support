import os
from colorama import Fore
import random
import asyncio

import disnake
from disnake.ext import commands
intents = disnake.Intents.default()
intents.members = True
from dotenv import load_dotenv
load_dotenv()

activity_list = [[disnake.ActivityType.watching, "👤 за пользователями"], [disnake.ActivityType.playing, "🎮 play.cmt-minecraft.ru"], [disnake.ActivityType.watching, "🔗 discord.gg/cmt-minecraft"], [disnake.ActivityType.streaming, "📺 play.cmt-minecraft.ru c Just_Pivko", "https://www.twitch.tv/just_pivko"]]

token = os.getenv("TOKEN")

bot = commands.InteractionBot(intents=intents)

async def presence_changer():
    while True:
        rng = random.randint(0, len(activity_list) - 1)
        if activity_list[rng][0] == disnake.ActivityType.streaming:
            activity = disnake.Activity(type=activity_list[rng][0], name=activity_list[rng][1], url=activity_list[rng][2])
        else:
            activity = disnake.Activity(type=activity_list[rng][0], name=activity_list[rng][1])
        await bot.change_presence(activity=activity)
        await asyncio.sleep(10)

@bot.event
async def on_ready():
    print(Fore.GREEN + f"[MAIN]: {bot.user} запущен.")
    print(Fore.WHITE + "--------------")
    await bot.get_channel(1198211964476850267).connect()
    await presence_changer()

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"[MAIN] cogs.{filename[:-3]} загружен")

bot.run(os.getenv('TOKEN'))