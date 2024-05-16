import random

import disnake
from disnake.ext import commands
from databases import user_base
import json
import datetime


def add_to_json(value: any, filename: str) -> None:
    with open(f"src/data/{filename}.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        c_data.append(value)

    with open(f"src/data/{filename}.json", "w", encoding="utf-8") as f:
        json.dump(c_data, f)


def get_values(filename: str) -> any:
    with open(f"src/data/{filename}.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        return c_data


level_users = {"646464": (123, 123)}


class LevelUpper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, inter: disnake.MessageInteraction):
        channels = get_values("level")
        if not str(inter.channel.id) in channels and not inter.author.bot:
            db = user_base.Database(inter.author.guild, self.bot)
            timing = round(datetime.datetime.now().timestamp())
            print(timing, "DJDDH")
            add_multi = 0
            if str(inter.author.id) in level_users:
                print(level_users)
                times = (timing - level_users[str(inter.author.id)][1])
                print(times)
                if times >= 60:
                    print("DDDODIDIDI")
                    if times <= 120:
                        current_lvl_multi = level_users[str(inter.author.id)]
                        add_multi = round(current_lvl_multi[0] / 5)
                        level_users[str(inter.author.id)] = (current_lvl_multi[0] + 1, timing)
                    else:
                        add_multi = 0
                        del level_users[str(inter.author.id)]
                else:
                    return
            else:
                level_users[str(inter.author.id)] = (1, timing)

            level_points = random.randint(6, 15) + add_multi

            response = db.add_level_points(inter.author.id, level_points)

            if response[0] == 200:
                await inter.channel.send(f"Поздравляем, {inter.author.mention}! "
                                         f"Ты повысил свой **уровень до {response[1]}!**", delete_after=10)

    @commands.slash_command(name="set_level", dm_permission=False)
    @commands.default_member_permissions(administrator=True)
    async def set_level(self, inter: disnake.ApplicationCommandInteraction, level: int = 0,
                        user: disnake.Member = None):
        if user is None:
            user = inter.user
        print(user.id)
        db = user_base.Database(inter.user.guild, self.bot)

        db.set_user_level(user.id, level)
        await inter.response.send_message("Готово.", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(LevelUpper(bot))
