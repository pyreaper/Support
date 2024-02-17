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

    @commands.slash_command(name="rcon", description="Отправить RCON-команду", dm_permission=False)
    @commands.default_member_permissions(administrator=True)
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


    @commands.slash_command(name="access", description="Выдать проходку", dm_permission=False)
    @commands.default_member_permissions(administrator=True)
    async def add_wl(inter: disnake.CommandInteraction, nickname: str = "1", user: disnake.Member = "1"):
        try:
            if nickname != "1":
                with MCRcon(host=host, port=port, password=password, timeout=timeout) as mcr:
                    resp = mcr.command(f'easywl add {nickname}')
                if resp != "":
                    await inter.response.send_message(f'**Ответ:** ```{resp}```', ephemeral=True)
                else:
                    await inter.response.send_message(f'**Команда была отправлена, но пришёл пустой ответ.**', ephemeral=True)
            elif user != "1":
                nickname = user.name
                with MCRcon(host=host, port=port, password=password, timeout=timeout) as mcr:
                    resp = mcr.command(f'easywl add {nickname}')
                if resp != "":
                    await inter.response.send_message(f'**Ответ:** ```{resp}```', ephemeral=True)
                else:
                    await inter.response.send_message(f'**Команда была отправлена, но пришёл пустой ответ.**', ephemeral=True)
            else:
                await inter.response.send_message(f'Вы не указали ни один из параметров (никнейм или юзера).', ephemeral=True)
        except Exception as ex:
            print(ex)
            print(type(ex))
            await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)
            
            

def setup(bot: commands.Bot):
    bot.add_cog(RCGiver(bot))