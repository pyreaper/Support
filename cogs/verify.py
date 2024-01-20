import json
import random

import disnake
from disnake import TextInputStyle
from disnake.ext import commands

def add_to_json(key, value):
    with open("./data.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        c_data[key] = value

    with open("./data.json", "w", encoding="utf-8") as f:
        json.dump(c_data, f)


def get_value(key):
    with open("./data.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        print(c_data[key])
        return c_data[key]

senders = {}

def updateVerifyEmbed():
    embed = disnake.Embed(
        title="Настройки верификации",
        description=f"**Титул:** ``{get_value('title')}`` \n **Описание: \n** ```{get_value('description')}``` **Текст кнопки:** ``{get_value('buttontext')}`` \n **Количество символов в капче:** ``{get_value('numbersincaptcha')}`` \n **Роль участника:** <@&{str(get_value('role_id'))}> \n **Канал для отправки:** <#{str(get_value('channel_id'))}> \n **Картинка:** ``ниже в сообщении``"
    )
    embed.set_image(url=get_value("image"))
    return embed

class VerifyModal(disnake.ui.Modal):
    def __init__(self, captchacode: str):
        components = [
            disnake.ui.TextInput(
                label="Капча",
                placeholder=captchacode,
                custom_id="captcha",
                style=TextInputStyle.short,
                max_length=get_value("numbersincaptcha"),
                min_length=get_value("numbersincaptcha"),
                required=True,
            ),
            disnake.ui.TextInput(
                label="Никнейм в майнкрафт",
                placeholder="spon4k",
                custom_id="mcname",
                style=TextInputStyle.short,
                max_length=16,
                min_length=3,
                required=True,
            ),
        ]
        super().__init__(title="Верификация", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        try:
            print(senders[inter.user.id])
            print(senders)
            if inter.text_values["captcha"] == senders[inter.user.id]:
                senders.pop(inter.user.id)
                role = inter.guild.get_role(get_value("role_id"))
                print(senders)
                await inter.user.edit(nick=inter.text_values["mcname"])
                await inter.user.add_roles(role)
                await inter.response.send_message(content="Капча решена верно. Удачной игры на нашем сервере.")
            else:
                senders.pop(inter.user.id)
                await inter.response.send_message(content="Капча решена неверно! Попробуйте снова", ephemeral=True)
        except Exception as ex:
            print(ex)
            await inter.response.send_message(content=f"Произошла ошибка. Обратитесь к администратору, сообщив код ошибки: ``{str(ex)}``", ephemeral=True)
class VerifySettingsModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Титул",
                value=get_value("title"),
                custom_id="title",
                style=TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Описание",
                value=get_value("description"),
                custom_id="description",
                style=TextInputStyle.paragraph,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Текст кнопки",
                value=get_value("buttontext"),
                custom_id="buttontext",
                style=TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Количество символов в капче",
                value=str(get_value("numbersincaptcha")),
                custom_id="numbersincaptcha",
                style=TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Ссылка на картинку",
                placeholder="...",
                value=get_value("image"),
                custom_id="image",
                style=TextInputStyle.short,
                required=False,
            ),
        ]
        super().__init__(title="Настройки", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        print(inter.text_values.items())
        for key, value in inter.text_values.items():
            if value != '':
                if key == "numbersincaptcha":
                    add_to_json(key, int(value))
                else:
                    add_to_json(key, value)

        await inter.message.edit(embeds=[updateVerifyEmbed()])
        await inter.response.send_message("Настройки были успешно изменены. Нажмите на кнопку для переотправки сообщения.")

async def verify(inter):
    embed = disnake.Embed(
        title=get_value("title"),
        description=get_value("description")
    )
    embed.set_image(url=get_value("image"))
    sended_msg = await inter.send(embeds=[embed], components=[disnake.ui.Button(label=get_value("buttontext"), style=disnake.ButtonStyle.gray, custom_id="startcaptcha")])
    return sended_msg.id
class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="verifysettings", dm_permission=False)
    @commands.default_member_permissions(administrator=True)
    async def verifysettings(self, inter):
        await inter.response.send_message(embeds=[updateVerifyEmbed()], components=[disnake.ui.RoleSelect(custom_id="settingsroleselect", placeholder="Роль"), disnake.ui.ChannelSelect(custom_id="verifychannelselect", placeholder="Канал"), disnake.ui.Button(label="Изменить настройки", style=disnake.ButtonStyle.gray, custom_id="changesettings"), disnake.ui.Button(label="Отправить сообщение в канал", style=disnake.ButtonStyle.success, custom_id="sendmessage"), disnake.ui.Button(label="Удалить сообщение из канала", style=disnake.ButtonStyle.danger, custom_id="deletemessage")])

    @commands.Cog.listener("on_button_click")
    async def button_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ["startcaptcha", "changesettings", "sendmessage", "deletemessage"]:
            return

        if inter.component.custom_id == "startcaptcha":
            if inter.user.id not in senders: 
                  senders[inter.user.id] = str(random.randint(int("1" * get_value("numbersincaptcha")), int("9" * get_value("numbersincaptcha"))))
                  await inter.response.send_modal(modal=VerifyModal(str(senders[inter.user.id])))
        elif inter.component.custom_id == "changesettings":
            await inter.response.send_modal(modal=VerifySettingsModal())
        elif inter.component.custom_id == "sendmessage":
            try:
                if get_value("verify_msg_id") != 0:
                    channel = inter.guild.get_channel(get_value("channel_id"))
                    msg = await channel.fetch_message(get_value("verify_msg_id"))
                    await msg.delete()
                    add_to_json("verify_msg_id", 0)
                sendedmsgid = await verify(inter.guild.get_channel(get_value("channel_id")))
                await inter.response.send_message("Успешно", ephemeral=True)
                add_to_json("verify_msg_id", sendedmsgid)
            except Exception as ex:
                add_to_json("verify_msg_id", 0)
                await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Айди сообщения было сброшено (удалите предыдущее если таковое имеется сами). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)
        
        elif inter.component.custom_id == "deletemessage":
            try:
                if get_value("verify_msg_id") != 0:
                    channel = inter.guild.get_channel(get_value("channel_id"))
                    msg = await channel.fetch_message(get_value("verify_msg_id"))
                    await msg.delete()
                    add_to_json("verify_msg_id", 0)
                    await inter.response.send_message("Успешно", ephemeral=True)
                else:
                    await inter.response.send_message("Похоже, сообщение ещё не было отправлено. Отправьте его", ephemeral=True)
            except Exception as ex:
                add_to_json("verify_msg_id", 0)
                await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Айди сообщения было сброшено (удалите предыдущее если таковое имеется сами). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)

    @commands.Cog.listener("on_dropdown")
    async def dropdown_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ["settingsroleselect", "verifychannelselect"]:
            return

        if inter.component.custom_id == "settingsroleselect":
            selected_value = inter.values[0]
            add_to_json("role_id", int(selected_value))
            await inter.response.send_message("Роль была перевыбрана", ephemeral=True)
            await inter.message.edit(embeds=[updateVerifyEmbed()])
        elif inter.component.custom_id == "verifychannelselect":
            selected_value = inter.values[0]
            try:
                if get_value("verify_msg_id") != 0:
                    channel = inter.guild.get_channel(get_value("channel_id"))
                    msg = await channel.fetch_message(get_value("verify_msg_id"))
                    await msg.delete()
                    add_to_json("verify_msg_id", 0)
                add_to_json("channel_id", int(selected_value))
                await inter.response.send_message("Канал был перевыбран", ephemeral=True)
                await inter.message.edit(embeds=[updateVerifyEmbed()])
            except Exception as ex:
                add_to_json("verify_msg_id", 0)
                await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Айди сообщения было сброшено (удалите предыдущее если таковое имеется сами). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)
            
            

def setup(bot: commands.Bot):
    bot.add_cog(Verify(bot))