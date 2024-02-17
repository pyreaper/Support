import json
import random

import disnake
from disnake import TextInputStyle
from disnake.ext import commands

def add_to_promo_json(key, value):
    with open("./data/promocodes.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        c_data[key] = value

    with open("./data/promocodes.json", "w", encoding="utf-8") as f:
        json.dump(c_data, f)


def get_promo_value(key):
    with open("./data/promocodes.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        return c_data[key]


class PromoCodes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="promocode", description="Получить еженедельный промокод (только для CMT+)", dm_permission=False, aliases=["промокод", "promo"])
    async def promocode(self, inter: disnake.ApplicationCommandInteraction):
        role = disnake.utils.find(lambda r: r.name == 'CMT+', inter.guild.roles)
        if role in inter.user.roles:
            embed = disnake.Embed(
                title="Промокод",
                description=f"**Ваш промокод:** ```{get_promo_value('promocode')}``` \n **Администраторы обновляет его каждую неделю.**"
            )

            await inter.response.send_message(embeds=[embed], ephemeral=True)
        else:
            await inter.response.send_message("У вас нет CMT+. Если вы приобрели его, но его нет на дискорд сервере, откройте тикет", ephemeral=True)

    @commands.slash_command(name="setpromo", description="Получить еженедельный промокод (только для CMT+)", dm_permission=False, aliases=["промокод", "promo"])
    @commands.has_permissions(administrator=True)
    async def setpromo(self, inter: disnake.ApplicationCommandInteraction, promocode: str):
        add_to_promo_json("promocode", promocode)
        await inter.response.send_message(f"Промокод **{get_promo_value('promocode')}** успешно установлен", ephemeral=True)
            

def setup(bot: commands.Bot):
    bot.add_cog(PromoCodes(bot))