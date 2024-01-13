import time
import json

import disnake
from collections import defaultdict
from disnake.ext import commands
from disnake import TextInputStyle
import os
import random

from dotenv import load_dotenv
load_dotenv()

bot = commands.InteractionBot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

senders = {}

class MyModal(disnake.ui.Modal):
    def __init__(self, captchacode: str):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="Капча",
                placeholder=captchacode,
                custom_id="captcha",
                style=TextInputStyle.short,
                max_length=4,
                min_length=4,
                required=True,
            ),
            disnake.ui.TextInput(
                label="Никнейм в майнкрафт",
                placeholder="spon4k",
                custom_id="mcname",
                style=TextInputStyle.short,
                max_length=16,
                required=True,
            ),
        ]
        super().__init__(title="Верификация", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        await inter.message.delete()
        try:
            print(senders[inter.user.id])
            print(senders)
            if inter.text_values["captcha"] == senders[inter.user.id]:
                value = senders.pop(inter.user.id)
                print(senders)
                await inter.user.edit(nick=inter.text_values["mcname"])
                await inter.response.send_message(content=inter.text_values["mcname"])
            else:
                value = senders.pop(inter.user.id)
                await inter.response.send_message(content="Капча решена неверно!", ephemeral=True)
        except Exception as ex:
            await inter.response.send_message(content="Капча решена верно, но у меня нет прав чтобы изменить вам никнейм.", ephemeral=True)
            

@bot.slash_command(name="verify")
async def verify(inter):
    await inter.response.send_message(content="Сообщение было отправлено", ephemeral=True)
    await inter.channel.send(content=f"Вы хотите продолжить?", components=[disnake.ui.Button(label="Yes", style=disnake.ButtonStyle.success, custom_id="startcaptcha")])

@bot.listen("on_button_click")
async def help_listener(inter: disnake.MessageInteraction):
    if inter.component.custom_id not in ["startcaptcha"]:
        # We filter out any other button presses except
        # the components we wish to process.
        return

    if inter.component.custom_id == "startcaptcha":
        senders[inter.user.id] = str(random.randint(1111, 9999))
        await inter.response.send_modal(modal=MyModal(str(senders[inter.user.id])))

bot.run(os.getenv('TOKEN'))