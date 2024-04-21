import disnake
from disnake import TextInputStyle
from disnake.ext import commands
from rcon_connection import MCRcon

from dotenv import load_dotenv
import os
load_dotenv()

host = os.getenv("HOST")
port = int(os.getenv("PORT"))
password = os.getenv("PASSWORD")
timeout = int(os.getenv("TIMEOUT"))

class RCGiver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(dm_permission=False)
    @commands.default_member_permissions(administrator=True)
    async def minecraft(self, inter):
        pass

    @minecraft.sub_command(name="rcon", description="Отправить RCON-команду")
    async def rcon(inter: disnake.ApplicationCommandInteraction, command):
        try:
            with MCRcon(host=host, port=port, password=password, timeout=timeout) as mcr:
                resp = mcr.command(command)
            if resp != "":
                await inter.response.send_message(f'**Ответ:** ```{resp}```', ephemeral=True)
            else:
                await inter.response.send_message(f'**Команда была отправлена, но пришёл пустой ответ.**', ephemeral=True)
        except Exception as ex:
            print(ex)
            print(type(ex))
            await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)


    @minecraft.sub_command(name="access", description="Выдать проходку")
    async def add_wl(inter: disnake.CommandInteraction, nickname: str = "1", user: disnake.Member = "1"):
        try:
            if nickname != "1":
                pass
            elif user != "1":
                nickname = user.name
            else:
                await inter.response.send_message(f'Вы не указали ни один из параметров (никнейм или юзера).', ephemeral=True)
                return
            
            with MCRcon(host=host, port=port, password=password, timeout=timeout) as mcr:
                    resp = mcr.command(f'easywl add {nickname}')
                    if resp != "":
                        await inter.response.send_message(f'**Ответ:** ```{resp}```', ephemeral=True)
                    else:
                        await inter.response.send_message(f'**Команда была отправлена, но пришёл пустой ответ.**', ephemeral=True)
        except Exception as ex:
            print(ex)
            print(type(ex))
            await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)


    # Moderation

    @minecraft.sub_command(name="ban", description="Выдать бан игроку")
    async def ban(inter: disnake.CommandInteraction, nickname: str = "1", user: disnake.Member = "1", reason: str = "не указана", logneed: str = commands.Param(choices=["Да", "Нет"])):
        try:
            reason = f"Discord, моднейм: {inter.user.name}, причина: {reason}"
            
            if nickname != "1":
                pass
            elif user != "1":
                nickname = user.name
            else:
                await inter.response.send_message(f'Вы не указали ни один из параметров (никнейм или юзера).', ephemeral=True)
                return
            
            with MCRcon(host=host, port=port, password=password, timeout=timeout) as mcr:
                    resp = mcr.command(f'lban {nickname} {reason}')
                    if logneed == "Да":
                        if resp != "":
                            await inter.response.send_message(f'**Ответ:** ```{resp}```', ephemeral=True)
                        else:
                            await inter.response.send_message(f'**Команда была отправлена, но пришёл пустой ответ.**', ephemeral=True)
        except Exception as ex:
            print(ex)
            print(type(ex))
            await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)

    @minecraft.sub_command(name="unban", description="Разбанить игрока")
    async def unban(inter: disnake.CommandInteraction, nickname: str = "1", user: disnake.Member = "1", reason: str = "не указана", logneed: str = commands.Param(choices=["Да", "Нет"])):
        try:
            reason = f"Discord, моднейм: {inter.user.name}, причина: {reason}"
            
            if nickname != "1":
                pass
            elif user != "1":
                nickname = user.name
            else:
                await inter.response.send_message(f'Вы не указали ни один из параметров (никнейм или юзера).', ephemeral=True)
                return
            
            with MCRcon(host=host, port=port, password=password, timeout=timeout) as mcr:
                    resp = mcr.command(f'lunban {nickname} {reason}')
                    if logneed == "Да":
                        if resp != "":
                            await inter.response.send_message(f'**Ответ:** ```{resp}```', ephemeral=True)
                        else:
                            await inter.response.send_message(f'**Команда была отправлена, но пришёл пустой ответ.**', ephemeral=True)
        except Exception as ex:
            print(ex)
            print(type(ex))
            await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)

    
    @minecraft.sub_command(name="mute", description="Замьютить игрока")
    async def mute(inter: disnake.CommandInteraction, nickname: str = "1", user: disnake.Member = "1", reason: str = "не указана", logneed: str = commands.Param(choices=["Да", "Нет"]), часы: int = 0, минуты: int = 0, секунды: int = 1):
        try:
            reason = f"Discord, моднейм: {inter.user.name}, причина: {reason}"

            timeinseconds = ((часы*3600) + (минуты*60) + секунды)
            
            if nickname != "1":
                pass
            elif user != "1":
                nickname = user.name
            else:
                await inter.response.send_message(f'Вы не указали ни один из параметров (никнейм или юзера).', ephemeral=True)
                return
            
            with MCRcon(host=host, port=port, password=password, timeout=timeout) as mcr:
                    resp = mcr.command(f'lmute {nickname} {timeinseconds}s {reason}')
                    if logneed == "Да":
                        if resp != "":
                            await inter.response.send_message(f'**Ответ:** ```{resp}```', ephemeral=True)
                        else:
                            await inter.response.send_message(f'**Команда была отправлена, но пришёл пустой ответ.**', ephemeral=True)
        except Exception as ex:
            print(ex)
            print(type(ex))
            await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)

    @minecraft.sub_command(name="unmute", description="Размьютить игрока")
    async def unmute(inter: disnake.CommandInteraction, nickname: str = "1", user: disnake.Member = "1", reason: str = "не указана", logneed: str = commands.Param(choices=["Да", "Нет"])):
        try:
            reason = f"Discord, моднейм: {inter.user.name}, причина: {reason}"
            
            if nickname != "1":
                pass
            elif user != "1":
                nickname = user.name
            else:
                await inter.response.send_message(f'Вы не указали ни один из параметров (никнейм или юзера).', ephemeral=True)
                return
            
            with MCRcon(host=host, port=port, password=password, timeout=timeout) as mcr:
                    resp = mcr.command(f'lunmute {nickname} {reason}')
                    if logneed == "Да":
                        if resp != "":
                            await inter.response.send_message(f'**Ответ:** ```{resp}```', ephemeral=True)
                        else:
                            await inter.response.send_message(f'**Команда была отправлена, но пришёл пустой ответ.**', ephemeral=True)
        except Exception as ex:
            print(ex)
            print(type(ex))
            await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)

    @minecraft.sub_command(name="warn", description="Выдать варн игроку")
    async def warn(inter: disnake.CommandInteraction, nickname: str = "1", user: disnake.Member = "1", reason: str = "не указана", logneed: str = commands.Param(choices=["Да", "Нет"])):
        try:
            reason = f"Discord, моднейм: {inter.user.name}, причина: {reason}"
            
            if nickname != "1":
                pass
            elif user != "1":
                nickname = user.name
            else:
                await inter.response.send_message(f'Вы не указали ни один из параметров (никнейм или юзера).', ephemeral=True)
                return
            
            with MCRcon(host=host, port=port, password=password, timeout=timeout) as mcr:
                    resp = mcr.command(f'lwarn {nickname} {reason}')
                    if logneed == "Да":
                        if resp != "":
                            await inter.response.send_message(f'**Ответ:** ```{resp}```', ephemeral=True)
                        else:
                            await inter.response.send_message(f'**Команда была отправлена, но пришёл пустой ответ.**', ephemeral=True)
        except Exception as ex:
            print(ex)
            print(type(ex))
            await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)

    @minecraft.sub_command(name="unwarn", description="Снять варн у игрока")
    async def unwarn(inter: disnake.CommandInteraction, nickname: str = "1", user: disnake.Member = "1", reason: str = "не указана", logneed: str = commands.Param(choices=["Да", "Нет"])):
        try:
            reason = f"Discord, моднейм: {inter.user.name}, причина: {reason}"
            
            if nickname != "1":
                pass
            elif user != "1":
                nickname = user.name
            else:
                await inter.response.send_message(f'Вы не указали ни один из параметров (никнейм или юзера).', ephemeral=True)
                return
            
            with MCRcon(host=host, port=port, password=password, timeout=timeout) as mcr:
                    resp = mcr.command(f'lunwarn {nickname} {reason}')
                    if logneed == "Да":
                        if resp != "":
                            await inter.response.send_message(f'**Ответ:** ```{resp}```', ephemeral=True)
                        else:
                            await inter.response.send_message(f'**Команда была отправлена, но пришёл пустой ответ.**', ephemeral=True)
        except Exception as ex:
            print(ex)
            print(type(ex))
            await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)
            



def setup(bot: commands.Bot):
    bot.add_cog(RCGiver(bot))