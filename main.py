import disnake
from disnake.ext import commands
from disnake import TextInputStyle
import os
import random
import json

def add_to_json(key, value):
    with open("data.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        c_data[key] = value

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(c_data, f)


def get_value(key):
    with open("data.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        print(c_data[key])
        return c_data[key]

from dotenv import load_dotenv
load_dotenv()

bot = commands.InteractionBot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

senders = {}

def updateVerifyEmbed():
    embed = disnake.Embed(
        title="Настройки верификации",
        description=f"**Титул:** ``{get_value('title')}`` \n **Описание: \n** ```{get_value('description')}``` **Текст кнопки:** ``{get_value('buttontext')}`` \n **Количество символов в капче:** ``{get_value('numbersincaptcha')}`` \n **Картинка:** ``ниже в сообщении``"
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
                value = senders.pop(inter.user.id)
                print(senders)
                await inter.user.edit(nick=inter.text_values["mcname"])
                await inter.response.send_message(content="Верификация успешно пройдена. Удачного времяпрепровождения!", ephemeral=True)
            else:
                value = senders.pop(inter.user.id)
                await inter.response.send_message(content="Капча решена неверно! Попробуйте снова", ephemeral=True)
        except Exception as ex:
            await inter.response.send_message(content="Капча решена верно, но у меня нет прав чтобы изменить вам никнейм. Если эта ошибка повторяется, обратитесь к администратору", ephemeral=True)

class VerifySettingsModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Титул",
                placeholder=get_value("title"),
                custom_id="title",
                style=TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Описание",
                placeholder="Чтобы пройти верификацию, ...",
                custom_id="description",
                style=TextInputStyle.paragraph,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Текст кнопки",
                placeholder=get_value("buttontext"),
                custom_id="buttontext",
                style=TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Количество символов в капче",
                placeholder=str(get_value("numbersincaptcha")),
                custom_id="numbersincaptcha",
                style=TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Ссылка на картинку",
                placeholder="...",
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
        await inter.response.send_message("Настройки были успешно изменены. Пропишите /verify в нужном вам канале для нового сообщения.")
            

@bot.slash_command(name="verify", dm_permission=False)
@commands.default_member_permissions(administrator=True)
async def verify(inter):
    embed = disnake.Embed(
        title=get_value("title"),
        description=get_value("description")
    )
    embed.set_image(url=get_value("image"))
    await inter.channel.send(embeds=[embed], components=[disnake.ui.Button(label=get_value("buttontext"), style=disnake.ButtonStyle.gray, custom_id="startcaptcha")])
    await inter.response.send_message("Сообщение было успешно отправлено.", ephemeral=True)

@bot.slash_command(name="verifysettings", dm_permission=False)
@commands.default_member_permissions(administrator=True)
async def verifysettings(inter):
    await inter.response.send_message(embeds=[updateVerifyEmbed()], components=[disnake.ui.Button(label="Изменить настройки", style=disnake.ButtonStyle.gray, custom_id="changesettings")])

@bot.listen("on_button_click")
async def help_listener(inter: disnake.MessageInteraction):
    if inter.component.custom_id not in ["startcaptcha", "changesettings"]:
        return

    if inter.component.custom_id == "startcaptcha":
        if inter.user.id not in senders: senders[inter.user.id] = str(random.randint(int("1" * get_value("numbersincaptcha")), int("9" * get_value("numbersincaptcha"))))
        await inter.response.send_modal(modal=VerifyModal(str(senders[inter.user.id])))
    elif inter.component.custom_id == "changesettings":
        await inter.response.send_modal(modal=VerifySettingsModal())

bot.run(os.getenv('TOKEN'))