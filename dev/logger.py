import disnake
from disnake.ext import commands
import json

def add_to_logger_json(key, value):
    with open("./data/logger.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        c_data[key] = value

    with open("./data/logger.json", "w", encoding="utf-8") as f:
        json.dump(c_data, f)


def get_logger_value(key):
    with open("./data/logger.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        return c_data[key]

def loadEmbed():
    embed = disnake.Embed(
        title="Настройки логгера",
        description=""
    )


#def setup(bot: commands.Bot):
    #bot.add_cog(Logger(bot))