import json
import os
import random

import disnake
from disnake.ext import commands
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("TOKEN")
      

bot = commands.InteractionBot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

bot.load_extension("cogs.verify")


bot.run(os.getenv('TOKEN'))