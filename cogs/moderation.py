import datetime

import disnake
from disnake import TextInputStyle
from disnake.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="kick", description="Кикнуть пользователя", dm_permission=False)
    @commands.default_member_permissions(kick_members=True)
    async def kick(self, inter, пользователь: disnake.Member, причина):
        """
        Parameters
        ----------
        user: :class:`disnake.User`
            Пользователь
        reason: :class:`str`
            Причина
        """
        try:
            embed = disnake.Embed(
                title="Вы были кикнуты с CMT"
            )
            embed.set_footer(text="©️ CMT. All rigts reserved", icon_url="https://cdn.discordapp.com/attachments/1195449612669038612/1195964735921868860/image.png?ex=65b5e7f4&is=65a372f4&hm=27bf36168a83249bf9c4b0bd94491bb525cca32896dc8ef884c688f5e6775c10&")
            embed.add_field(name="Причина", value=f"> ```{причина}```", inline=False)
            embed.add_field(name="Модератор", value=f"> ```{inter.user.name}```", inline=False)
            await пользователь.send(embeds=[embed], components=[disnake.ui.Button(label="Наш сайт", style=disnake.ButtonStyle.link, url="https://cmt-minecraft.ru")])
            await пользователь.kick(reason=причина)
            await inter.response.send_message("Пользователь был кикнут с сервера")
        except Exception as ex:
                await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)

    @commands.slash_command(name="ban", description="Забанить пользователя", dm_permission=False)
    @commands.default_member_permissions(ban_members=True)
    async def ban(self, inter, пользователь: disnake.Member, причина):
        """
        Parameters
        ----------
        user: :class:`disnake.User`
            Пользователь
        reason: :class:`str`
            Причина
        """
        try:
            embed = disnake.Embed(
                title="Вы были забанены на CMT"
            )
            embed.set_footer(text="©️ CMT. All rigts reserved", icon_url="https://cdn.discordapp.com/attachments/1195449612669038612/1195964735921868860/image.png?ex=65b5e7f4&is=65a372f4&hm=27bf36168a83249bf9c4b0bd94491bb525cca32896dc8ef884c688f5e6775c10&")
            embed.add_field(name="Причина", value=f"> ```{причина}```", inline=False)
            embed.add_field(name="Модератор", value=f"> ```{inter.user.name}```", inline=False)
            await пользователь.send(embeds=[embed], components=[disnake.ui.Button(label="Наш сайт", style=disnake.ButtonStyle.link, url="https://cmt-minecraft.ru")])
            await пользователь.ban(reason=причина)
            await inter.response.send_message("Пользователь был отправлен в таймаут")
        except Exception as ex:
                await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)

    @commands.slash_command(name="mute", description="Замутить юзера", dm_permission=False)
    @commands.default_member_permissions(kick_members=True)
    async def timeout(self, inter, пользователь: disnake.Member, причина, часы: int = 0, минуты: int = 0, секунды: int = 1):
        """
        Parameters
        ----------
        user: :class:`disnake.User`
            Пользователь
        reason: :class:`str`
            Причина
        hours: :class:`int`
            Часы
        minutes: :class:`int`
            Минуты
        seconds: :class:`int`
            Секунды
        """
        try:
            embed = disnake.Embed(
                title="Вам выдан мут на CMT"
            )
            embed.set_footer(text="©️ CMT. All rigts reserved", icon_url="https://cdn.discordapp.com/attachments/1195449612669038612/1195964735921868860/image.png?ex=65b5e7f4&is=65a372f4&hm=27bf36168a83249bf9c4b0bd94491bb525cca32896dc8ef884c688f5e6775c10&")
            embed.add_field(name="Причина", value=f"> ```{причина}```", inline=False)
            embed.add_field(name="Длительность", value=f"```Часы: {str(часы)},\nМинуты: {str(минуты)}\nСекунды: {str(секунды)}```", inline=False)
            embed.add_field(name="Модератор", value=f"> ```{inter.user.name}```", inline=False)
            await пользователь.send(embeds=[embed], components=[disnake.ui.Button(label="Наш сайт", style=disnake.ButtonStyle.link, url="https://cmt-minecraft.ru")])
            await пользователь.timeout(duration=datetime.timedelta(hours=часы, minutes=минуты, seconds=секунды), reason=причина)
            await inter.response.send_message(f"Пользователь был отправлен в мут на {часы} часов, {минуты} минут, {секунды} секунд")
        except Exception as ex:
                await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)
    
            

def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))