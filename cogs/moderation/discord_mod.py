import datetime
import json

import disnake
from disnake import TextInputStyle
from disnake.ext import commands

import asyncio

def get_warn_value(user):
    with open("./data/moderation.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        if str(user) not in c_data:
            return 0
        else:
            return c_data[str(user)]
    
def warn_to_json(user):
    with open("./data/moderation.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        if str(user) not in c_data:
            c_data[str(user)] = 1
        else:
            c_data[str(user)] += 1

    with open("./data/moderation.json", "w", encoding="utf-8") as f:
        json.dump(c_data, f)

def unwarn_user(user):
    with open("./data/moderation.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        if str(user) not in c_data:
            return 0
        else:
            c_data[str(user)] -= 1

    with open("./data/moderation.json", "w", encoding="utf-8") as f:
        json.dump(c_data, f)
    
    return 1

async def check_if_can(user) -> bool:
    try:
        await user.send()
    except disnake.errors.Forbidden:
        return False
    except disnake.errors.HTTPException:
        return True
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(dm_permission=False)
    @commands.default_member_permissions(kick_members=True, ban_members=True)
    async def discord(self, inter):
        pass

    @commands.slash_command(dm_permission=False)
    @commands.default_member_permissions(administrator=True)
    async def admin(self, inter):
        pass

    # Kicks and bans

    @discord.sub_command(name="kick", description="Кикнуть пользователя")
    async def kick(self, inter, пользователь: disnake.Member, причина):
        if пользователь == inter.user:
            await inter.response.send_message("Вы не можете кикнуть сами себя.")
            return

        if пользователь.top_role >= inter.user.top_role:
            await inter.response.send_message("Вы не можете кикнуть этого пользователя, так как у него/нее роль выше вашей.")
            return
        
        if пользователь.bot == True:
            await inter.response.send_message("Вы не можете кикнуть бота. Если вам понадобилось его кикнуть, сделайте это вручную.")
            return

        try:
            if check_if_can(user=пользователь):
                embed = disnake.Embed(
                    title="Вы были кикнуты с Mithic Vanilla"
                )
                embed.set_footer(text="©️ Mithic Vanilla. All rigts reserved", icon_url="https://cdn.discordapp.com/attachments/1105911982873378816/1222136596174733382/image.png?ex=661e58e6&is=660be3e6&hm=e99c9c3e143c41da23f5d07fd5b481c3e968c60c8de627bd859ec8cff4f6060f&")
                embed.add_field(name="Причина", value=f"> ```{причина}```", inline=False)
                embed.add_field(name="Модератор", value=f"> ```{inter.user.name}```", inline=False)
                await пользователь.send(embeds=[embed], components=[disnake.ui.Button(label="Наш сайт", style=disnake.ButtonStyle.link, url="https://mithic.ru/")])
            await пользователь.kick(reason=причина)
            await inter.response.send_message("Пользователь был кикнут с сервера")
        except Exception as ex:
                await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)


    @discord.sub_command(name="ban", description="Забанить пользователя")
    async def ban(self, inter, пользователь: disnake.Member, причина):
        if пользователь == inter.user:
            await inter.response.send_message("Вы не можете забанить сами себя.")
            return

        if пользователь.top_role >= inter.user.top_role:
            await inter.response.send_message("Вы не можете забанить этого пользователя, так как у него/нее роль выше вашей.")
            return
        
        if пользователь.bot == True:
            await inter.response.send_message("Вы не можете забанить бота. Если вам понадобилось его забанить, сделайте это вручную.")
            return

        try:
            if check_if_can(user=пользователь):
                embed = disnake.Embed(
                    title="Вы были забанены на Mithic Vanilla"
                )
                embed.set_footer(text="©️ Mithic Vanilla. All rigts reserved", icon_url="https://cdn.discordapp.com/attachments/1105911982873378816/1222136596174733382/image.png?ex=661e58e6&is=660be3e6&hm=e99c9c3e143c41da23f5d07fd5b481c3e968c60c8de627bd859ec8cff4f6060f&")
                embed.add_field(name="Причина", value=f"> ```{причина}```", inline=False)
                embed.add_field(name="Модератор", value=f"> ```{inter.user.name}```", inline=False)
                await пользователь.send(embeds=[embed], components=[disnake.ui.Button(label="Наш сайт", style=disnake.ButtonStyle.link, url="https://mithic.ru/")])
            await пользователь.ban(reason=причина)
            await inter.response.send_message("Пользователь был забанен")
        except Exception as ex:
                await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)


    @discord.sub_command(name="unban", description="Разбанить пользователя")
    async def unban(self, inter, id: str):
        try:
            user_id = int(id)

            guild = inter.guild
            banned_users = guild.bans()
            print(banned_users)

            async for ban_entry in banned_users:
                if ban_entry.user.id == user_id:
                    await guild.unban(ban_entry.user)
                    await inter.response.send_message("Пользователь был разбанен")
        except Exception as ex:
           if ex == "404 Not Found (error code: 10026): Unknown Ban":
               await inter.response.send_message(f"Пользователь не забанен", ephemeral=True)
           else:
                await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)

    # Mutes
    
    @discord.sub_command(name="mute", description="Замьютить юзера")
    async def timeout(self, inter, пользователь: disnake.Member, причина, часы: int = 0, минуты: int = 0, секунды: int = 1):
        if пользователь == inter.user:
            await inter.response.send_message("Вы не можете замьютить сами себя.")
            return

        if пользователь.top_role >= inter.user.top_role:
            await inter.response.send_message("Вы не можете замьютить этого пользователя, так как у него/нее роль выше вашей.")
            return
        
        if пользователь.bot == True:
            await inter.response.send_message("Вы не можете замьютить бота.")
            return
        
        if пользователь.guild_permissions.administrator == True:
            await inter.response.send_message("Вы не можете замьютить администратора.")
            return

        try:
            if check_if_can(user=пользователь):
                embed = disnake.Embed(
                    title="Вам выдан мьют на Mithic Vanilla"
                )
                embed.set_footer(text="©️ Mithic Vanilla. All rigts reserved", icon_url="https://cdn.discordapp.com/attachments/1105911982873378816/1222136596174733382/image.png?ex=661e58e6&is=660be3e6&hm=e99c9c3e143c41da23f5d07fd5b481c3e968c60c8de627bd859ec8cff4f6060f&")
                embed.add_field(name="Причина", value=f"> ```{причина}```", inline=False)
                embed.add_field(name="Длительность", value=f"```Часы: {str(часы)},\nМинуты: {str(минуты)}\nСекунды: {str(секунды)}```", inline=False)
                embed.add_field(name="Модератор", value=f"> ```{inter.user.name}```", inline=False)
                await пользователь.send(embeds=[embed], components=[disnake.ui.Button(label="Наш сайт", style=disnake.ButtonStyle.link, url="https://mithic.ru/")])
            await пользователь.timeout(duration=datetime.timedelta(hours=часы, minutes=минуты, seconds=секунды), reason=причина)
            await inter.response.send_message(f"Пользователь был отправлен в мут на {часы} часов, {минуты} минут, {секунды} секунд")
        except Exception as ex:
            await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)


    @discord.sub_command(name="unmute", description="Размьютить юзера")
    async def un_timeout(self, inter, пользователь: disnake.Member, причина):
        if пользователь.bot == True:
            await inter.response.send_message("Вы не можете размьютить бота.")
            return
        
        if пользователь.current_timeout == None:
            await inter.response.send_message("Этот пользователь не замьючен.")
            return

        try:
            if check_if_can(user=пользователь):
                embed = disnake.Embed(
                    title="Вас размьютили"
                )
                embed.set_footer(text="©️ Mithic Vanilla. All rigts reserved", icon_url="https://cdn.discordapp.com/attachments/1105911982873378816/1222136596174733382/image.png?ex=661e58e6&is=660be3e6&hm=e99c9c3e143c41da23f5d07fd5b481c3e968c60c8de627bd859ec8cff4f6060f&")
                embed.add_field(name="Причина", value=f"> ```{причина}```", inline=False)
                embed.add_field(name="Модератор", value=f"> ```{inter.user.name}```", inline=False)
                await пользователь.send(embeds=[embed], components=[disnake.ui.Button(label="Наш сайт", style=disnake.ButtonStyle.link, url="https://mithic.ru/")])
            await пользователь.timeout(reason=причина, until=None)
            await inter.response.send_message(f"Пользователь был размьючен.")
        except Exception as ex:
            await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)



    # Warns
    
    @discord.sub_command(name="warn", description="Выдать варн пользователю")
    async def warn(self, inter, пользователь: disnake.Member, причина: str):
        if пользователь == inter.user:
            await inter.response.send_message("Вы не можете дать варн самому себе.")
            return

        if пользователь.top_role >= inter.user.top_role:
            await inter.response.send_message("Вы не можете дать варн этому пользователю, так как у него/нее роль выше вашей.")
            return
        
        if пользователь.bot == True:
            await inter.response.send_message("Вы не можете дать варн боту.")
            return

        try:
            if check_if_can(user=пользователь):
                embed = disnake.Embed(
                    title="Вам выдан варн на Mithic Vanilla"
                )
                embed.set_footer(text="©️ Mithic Vanilla. All rigts reserved", icon_url="https://cdn.discordapp.com/attachments/1105911982873378816/1222136596174733382/image.png?ex=661e58e6&is=660be3e6&hm=e99c9c3e143c41da23f5d07fd5b481c3e968c60c8de627bd859ec8cff4f6060f&")
                embed.add_field(name="Причина", value=f"> ```{причина}```", inline=False)
                embed.add_field(name="Модератор", value=f"> ```{inter.user.name}```", inline=False)
                embed.add_field(name="Всего у вас варнов", value=f"> ```{str(get_warn_value(пользователь.id))}```", inline=False)
                await пользователь.send(embeds=[embed], components=[disnake.ui.Button(label="Наш сайт", style=disnake.ButtonStyle.link, url="https://mithic.ru/")])
            warn_to_json(пользователь.id)
            if get_warn_value(пользователь.id) >= 3:
                if get_warn_value(пользователь.id) <= 6:
                    await inter.response.send_message(f"Пользователю успешно выдан варн и он отправлен в мут на {str(get_warn_value(пользователь.id))} час(-ов)")
                    await self.bot.get_slash_command("admin silentmute").callback(self=self, inter=inter, пользователь=пользователь, причина="Автомод: за большое количество варнов", часы=get_warn_value(пользователь.id))
                else:
                    await inter.response.send_message(f"Пользователю успешно выдан варн и он был забанен навсегда")
                    await self.bot.get_slash_command("admin silentban").callback(self=self, inter=inter, пользователь=пользователь, автомод=True)
            else:
                await inter.response.send_message(f"Пользователю успешно выдан варн.")
        except Exception as ex:
            await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)
    

    @discord.sub_command(name="unwarn", description="Снять пред")
    async def unwarn(self, inter, пользователь: disnake.Member, причина: str):
        if пользователь == inter.user:
            await inter.response.send_message("Вы не можете снять варн у себя же.")
            return

        if пользователь.top_role >= inter.user.top_role:
            await inter.response.send_message("Вы не можете снять варн этому пользователю, так как у него/нее роль выше вашей.")
            return
        
        if пользователь.bot == True:
            await inter.response.send_message("Вы не можете снять варн у бота.")

        try:
            if unwarn_user(пользователь.id) == 1:
                if check_if_can(user=пользователь):
                    embed = disnake.Embed(
                        title="Вам снят варн на Mithic Vanilla"
                    )
                    embed.set_footer(text="©️ Mithic Vanilla. All rigts reserved", icon_url="https://cdn.discordapp.com/attachments/1105911982873378816/1222136596174733382/image.png?ex=661e58e6&is=660be3e6&hm=e99c9c3e143c41da23f5d07fd5b481c3e968c60c8de627bd859ec8cff4f6060f&")
                    embed.add_field(name="Причина", value=f"> ```{причина}```", inline=False)
                    embed.add_field(name="Модератор", value=f"> ```{inter.user.name}```", inline=False)
                    embed.add_field(name="Всего у вас варнов", value=f"> ```{str(get_warn_value(пользователь.id))}```", inline=False)
                    await пользователь.send(embeds=[embed], components=[disnake.ui.Button(label="Наш сайт", style=disnake.ButtonStyle.link, url="https://mithic.ru/")])
                await inter.response.send_message(f"Пользователю успешно снят варн.")
            else:
                await inter.response.send_message(f"У пользователя нет варнов")
        except Exception as ex:
            await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)


    @discord.sub_command(name="warns", description="Посмотреть преды")
    async def warns(self, inter, пользователь: disnake.Member):
        if пользователь.bot == True:
            await inter.response.send_message("Вы не можете посмотреть варны у бота.")

        try:
            embed = disnake.Embed(
                title="Варны",
                description=f"**Всего варнов: {str(get_warn_value(пользователь.id))}**"
            )
            embed.set_footer(text="©️ Mithic Vanilla. All rigts reserved", icon_url="https://cdn.discordapp.com/attachments/1105911982873378816/1222136596174733382/image.png?ex=661e58e6&is=660be3e6&hm=e99c9c3e143c41da23f5d07fd5b481c3e968c60c8de627bd859ec8cff4f6060f&")
            await inter.response.send_message(embeds=[embed], components=[disnake.ui.Button(label="Наш сайт", style=disnake.ButtonStyle.link, url="https://mithic.ru/")])
        except Exception as ex:
            await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)



    # Silent commands

    @admin.sub_command(name="silentban", description="Сайлент команда бана")
    async def silent_ban(self, inter, пользователь: disnake.Member, автомод: bool = False):
        if пользователь == inter.user:
            await inter.channel.send("Лог: ошибка")
            return
        
        if пользователь.bot == True:
            await inter.channel.send("Лог: ошибка")
            return

        try:
            if автомод:
                can = await check_if_can(user=пользователь)
                if can:
                    await пользователь.send("Вы были забанены автомодом по причине: большое количество варнов.")
                    await пользователь.ban(reason=f"Автомод. Модератор: {inter.user.id}")
                else:
                    await пользователь.ban(reason=f"Автомод. Модератор: {inter.user.id}")
            else:
                await пользователь.ban(reason=f"Сайлент бан. Модератор: {inter.user.id}")
                await inter.channel.send("Лог: успешно")
        except Exception as ex:
                await inter.channel.send(f"Лог: ошибка. {ex}")

    
    @admin.sub_command(name="silentmute")
    async def silent_timeout(self, inter, пользователь: disnake.Member, причина, часы: int = 0, минуты: int = 0, секунды: int = 1):
        try:
            await пользователь.timeout(duration=datetime.timedelta(hours=часы, minutes=минуты, seconds=секунды), reason=причина)
        except Exception as ex:
            await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)
            


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))