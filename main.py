import os
import json
from colorama import Fore
import random
import asyncio

import disnake
from disnake.ext import commands
intents = disnake.Intents.default()
intents.members = True
from dotenv import load_dotenv
load_dotenv()

def get_voice_value():
    with open("./data/voice.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        return c_data["id"]
    
def voice_to_json(value):
    with open("./data/voice.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        c_data["id"] = value

    with open("./data/voice.json", "w", encoding="utf-8") as f:
        json.dump(c_data, f)

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
    try:
        if get_voice_value() != 0:
            await bot.get_channel(get_voice_value()).connect()
        else:
            pass
    except Exception as ex:
        print(ex)
        voice_to_json(0)
        pass
    await presence_changer()

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"[MAIN] cogs.{filename[:-3]} загружен")

@bot.slash_command(name="voiceconnect", description="Канал для подключения к войсу", dm_permission=False)
@commands.default_member_permissions(administrator=True)
async def verifysettings(inter, channel: disnake.VoiceChannel):
        if len(bot.voice_clients) != 0:
            for i in bot.voice_clients:
                await i.disconnect()
        voice_to_json(channel.id)
        await inter.response.send_message(f"Бот теперь будет подключаться к каналу <#{channel.id}>", ephemeral=True)
        await channel.connect()

bot.run(os.getenv('TOKEN'))