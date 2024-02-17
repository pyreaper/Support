import os
from colorama import Fore

import disnake
from disnake.ext import commands
intents = disnake.Intents.all()
intents.members = True
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("TOKEN")

bot = commands.InteractionBot(intents=intents)

game = disnake.Game(name="🎮 play.cmt-minecraft.ru")

@bot.event
async def on_ready():
    await bot.change_presence(activity=game, status=disnake.Status.dnd)
    print(Fore.GREEN + f"[MAIN]: {bot.user} запущен.")
    print(Fore.WHITE + "--------------")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"[MAIN] cogs.{filename[:-3]} загружен")

bot.run(os.getenv('TOKEN'))