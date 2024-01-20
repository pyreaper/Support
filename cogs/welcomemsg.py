import json
import random

import disnake
from disnake import TextInputStyle
from disnake.ext import commands

def add_to_welcome_json(key, value):
    with open("./data/welcome.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        c_data[key] = value

    with open("./data/welcome.json", "w", encoding="utf-8") as f:
        json.dump(c_data, f)


def get_welcome_value(key):
    with open("./data/welcome.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        return c_data[key]

senders = {}

def settingsWelcomeEmbed():
    embed = disnake.Embed(
        title="Настройки приветствия",
        description=f"**Титул:** ``{get_welcome_value('title')}`` \n **Описание: \n** ```{get_welcome_value('description')}``` \n **Канал для отправки:** <#{str(get_welcome_value('channel_id'))}> \n **Картинка:** ``ниже в сообщении``"
    )
    embed.set_image(url=get_welcome_value("image"))
    return embed

class WelcomeSettingsModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Титул",
                value=get_welcome_value("title"),
                custom_id="title",
                style=TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Описание",
                value=get_welcome_value("description"),
                custom_id="description",
                style=TextInputStyle.paragraph,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Ссылка на картинку",
                placeholder="...",
                value=get_welcome_value("image"),
                custom_id="image",
                style=TextInputStyle.short,
                required=False,
            ),
        ]
        super().__init__(title="Настройки", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        for key, value in inter.text_values.items():
            if value != '':
                add_to_welcome_json(key, value)

        await inter.message.edit(embeds=[settingsWelcomeEmbed()])
        await inter.response.send_message("Настройки были успешно изменены.", ephemeral=True)


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="welcomesettings", description="Настройки для приветствий", dm_permission=False)
    @commands.default_member_permissions(administrator=True)
    async def welcomesettings(self, inter):
        if get_welcome_value("off") == True:
            offbtn = disnake.ui.Button(label="Включить оповещения", style=disnake.ButtonStyle.success, custom_id="offbtn")
        else:
            offbtn = disnake.ui.Button(label="Отключить оповещения", style=disnake.ButtonStyle.danger, custom_id="offbtn")
        await inter.response.send_message(embeds=[settingsWelcomeEmbed()], components=[disnake.ui.ChannelSelect(custom_id="welcomechannelselect", placeholder="Канал"), disnake.ui.Button(label="Изменить настройки", style=disnake.ButtonStyle.gray, custom_id="changewelcomesettings"), offbtn])

    @commands.Cog.listener("on_button_click")
    async def button_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ["changewelcomesettings", "offbtn"]:
            return
        
        if inter.component.custom_id == "changewelcomesettings":
            await inter.response.send_modal(modal=WelcomeSettingsModal())
        elif inter.component.custom_id == "offbtn":
            add_to_welcome_json("off", not get_welcome_value("off"))
            await inter.response.send_message("Успешно", ephemeral=True)
            if get_welcome_value("off") == True:
                offbtn = disnake.ui.Button(label="Включить оповещения", style=disnake.ButtonStyle.success, custom_id="offbtn")
            else:
                offbtn = disnake.ui.Button(label="Отключить оповещения", style=disnake.ButtonStyle.danger, custom_id="offbtn")
            await inter.message.edit(embeds=[settingsWelcomeEmbed()], components=[disnake.ui.ChannelSelect(custom_id="welcomechannelselect", placeholder="Канал"), disnake.ui.Button(label="Изменить настройки", style=disnake.ButtonStyle.gray, custom_id="changesettings"), offbtn])
    
    @commands.Cog.listener("on_dropdown")
    async def dropdown_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ["welcomechannelselect"]:
            return

        if inter.component.custom_id == "welcomechannelselect":
            selected_value = inter.values[0]
            try:
                add_to_welcome_json("channel_id", int(selected_value))
                await inter.response.send_message("Канал был перевыбран", ephemeral=True)
                await inter.message.edit(embeds=[settingsWelcomeEmbed()])
            except Exception as ex:
                await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)
    

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member):
        if get_welcome_value("off") == False:
            channel = self.bot.get_channel(get_welcome_value("channel_id"))
            footers = ["🔗 discord.gg/cmt-minecraft", "🎮 play.cmt-minecraft.ru"]
            footer_rng = random.randint(0, len(footers) - 1)
            footer = footers[footer_rng]
            embed = disnake.Embed(
                title=get_welcome_value("title"),
                description=get_welcome_value("description"),
            )
            embed.set_footer(
                text=footer,
            )
            embed.set_image(url=get_welcome_value("image"))
            await channel.send(embeds=[embed], content=f"<@{member.id}>")

            

def setup(bot: commands.Bot):
    bot.add_cog(Welcome(bot))