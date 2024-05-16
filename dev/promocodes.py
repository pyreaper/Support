import disnake
from disnake.ext import commands

import json_storer as jsonclass

json_storer = jsonclass.JsonStorer("promocodes")


def get_promo_value(key):
    return json_storer.get_value(key)


def add_to_promo_json(key, value):
    json_storer.add_to_json(key, value)


class PromoCodes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="promocode", description="Получить еженедельный промокод (только для CMT+)",
                            dm_permission=False, aliases=["промокод", "promo"])
    async def promocode(self, inter: disnake.ApplicationCommandInteraction):
        role = disnake.utils.find(lambda r: r.name == 'CMT+', inter.guild.roles)
        if role in inter.user.roles:
            embed = disnake.Embed(
                title="Промокод",
                description=f"**Ваш промокод:** ```{get_promo_value('promocode')}``` \n **Администраторы обновляет его каждую неделю.**"
            )

            await inter.response.send_message(embeds=[embed], ephemeral=True)
        else:
            await inter.response.send_message(
                "У вас нет Apex. Если вы приобрели его, но его нет на дискорд сервере, откройте тикет", ephemeral=True)

    @commands.slash_command(name="setpromo", description="Получить еженедельный промокод (только для CMT+)",
                            dm_permission=False, aliases=["промокод", "promo"])
    @commands.has_permissions(administrator=True)
    async def setpromo(self, inter: disnake.ApplicationCommandInteraction, promocode: str):
        add_to_promo_json("promocode", promocode)
        await inter.response.send_message(f"Промокод **{get_promo_value('promocode')}** успешно установлен",
                                          ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(PromoCodes(bot))
