import os
from colorama import Fore

import disnake
from disnake.ext import commands
intents = disnake.Intents.all()
intents.members = True
from dotenv import load_dotenv
load_dotenv()

version = "2.2.5"
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

@bot.slash_command(name="ping", description="Пинг бота, и другая полезная информация")
async def ping(inter: disnake.ApplicationCommandInteraction):
    embed = disnake.Embed(
        title="🏓  Понг",
        description=f"> **🟢 Задержка бота: {round(bot.latency * 1000)}мс \n > <:cmt:1210629320356266005> Версия бота: {version}**"
    )

    embed.set_image(url="https://cdn.discordapp.com/attachments/1083744274912378884/1083747819845865593/line.png?ex=65eb16cf&is=65d8a1cf&hm=f04e5f39e348595fa4824fa1a3833f1feaaa7df21195ede7dd5d76d3529c47fe&")

    await inter.response.send_message(embeds=[embed], ephemeral=True)

bot.run(os.getenv('TOKEN'))