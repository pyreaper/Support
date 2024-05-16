import json_storer
import random

import disnake
from disnake import TextInputStyle
from disnake.ext import commands

def add_to_welcome_json(key, value):
    json_storer.add_to_json(key, value, "welcome")


def get_welcome_value(key):
    return json_storer.get_value(key, "welcome")

interaction_storage = {}

def settingsWelcomeEmbed():
    embed = disnake.Embed(
        title="Настройки приветствия",
        description=f"**Титул:** ``{get_welcome_value('title')}`` \n **Описание: \n** {get_welcome_value('description')} \n **Канал для отправки:** <#{str(get_welcome_value('channel_id'))}> \n **Картинка:** ``ниже в сообщении`` \n **Текст кнопки:** ``{get_welcome_value('button')}`` \n **Ссылка в кнопке:** ``{get_welcome_value('button_link')}``"
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

class WelcomeButtonSettingsModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Текст",
                custom_id="button",
                style=TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Ссылка",
                custom_id="button_link",
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
    async def welcomesettings(self, inter: disnake.ApplicationCommandInteraction):
        if get_welcome_value("off") == True:
            offbtn = disnake.ui.Button(label="Включить оповещения", style=disnake.ButtonStyle.success, custom_id="offbtn")
        else:
            offbtn = disnake.ui.Button(label="Отключить оповещения", style=disnake.ButtonStyle.danger, custom_id="offbtn")
        print(interaction_storage)
        await inter.response.send_message("Эмбед с настройками успешно отправлен", ephemeral=True)
        msg = await inter.channel.send(embeds=[settingsWelcomeEmbed()], components=[disnake.ui.ChannelSelect(custom_id="welcomechannelselect", placeholder="Канал", channel_types=[disnake.ChannelType.text]), disnake.ui.Button(label="Изменить настройки", style=disnake.ButtonStyle.gray, custom_id="changewelcomesettings"), disnake.ui.Button(label="Изменить кнопку", style=disnake.ButtonStyle.gray, custom_id="changewelcomebutton"), disnake.ui.Button(label="Отправить тестовое сообщение", style=disnake.ButtonStyle.success, custom_id="sendtestwelcomemessage"), offbtn])
        print(msg)
        if inter.user.id not in interaction_storage:
            interaction_storage[inter.author.id] = [msg.id]
        else:
            interaction_storage[inter.author.id].append(msg.id)

    @commands.Cog.listener("on_button_click")
    async def button_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ["changewelcomesettings", "changewelcomebutton", "offbtn", "sendtestwelcomemessage"]:
            return
        
        if inter.user.id in interaction_storage and inter.message.id in interaction_storage[inter.user.id]:
            if inter.component.custom_id == "changewelcomesettings":
                await inter.response.send_modal(modal=WelcomeSettingsModal())
            elif inter.component.custom_id == "changewelcomebutton":
                await inter.response.send_modal(modal=WelcomeButtonSettingsModal())
            elif inter.component.custom_id == "sendtestwelcomemessage":
                footers = ["🔗 discord.gg/cmt-minecraft", "🎮 play.cmt-minecraft.ru"]
                footer_rng = random.randint(0, len(footers) - 1)
                footer = footers[footer_rng]
                button = None
                if get_welcome_value("button") != "0" and get_welcome_value("button_link") != "0":
                    button = disnake.ui.Button(label=get_welcome_value("button"), style=disnake.ButtonStyle.link, url=get_welcome_value("button_link"))
                embed = disnake.Embed(
                    title=get_welcome_value("title"),
                    description=get_welcome_value("description"),
                )
                embed.set_footer(
                    text=footer,
                )
                embed.set_image(url=get_welcome_value("image"))
                if button != None:
                    await inter.response.send_message(embeds=[embed], content=f"<@{inter.user.id}>", components=[button], ephemeral=True)
                else:
                    await inter.response.send_message(embeds=[embed], content=f"<@{inter.user.id}>", ephemeral=True)
            elif inter.component.custom_id == "offbtn":
                add_to_welcome_json("off", not get_welcome_value("off"))
                await inter.response.send_message("Успешно", ephemeral=True)
                if get_welcome_value("off") == True:
                    offbtn = disnake.ui.Button(label="Включить оповещения", style=disnake.ButtonStyle.success, custom_id="offbtn")
                else:
                    offbtn = disnake.ui.Button(label="Отключить оповещения", style=disnake.ButtonStyle.danger, custom_id="offbtn")
                await inter.message.edit(embeds=[settingsWelcomeEmbed()], components=[disnake.ui.ChannelSelect(custom_id="welcomechannelselect", placeholder="Канал"), disnake.ui.Button(label="Изменить настройки", style=disnake.ButtonStyle.gray, custom_id="changesettings"), disnake.ui.Button(label="Изменить настройки", style=disnake.ButtonStyle.gray, custom_id="changewelcomesettings"), disnake.ui.Button(label="Изменить кнопку", style=disnake.ButtonStyle.gray, custom_id="changewelcomebutton"), disnake.ui.Button(label="Отправить тестовое сообщение", style=disnake.ButtonStyle.success, custom_id="sendtestwelcomemessage"), offbtn])
        else:
            print(inter.id in interaction_storage, inter.message.id, inter.user.id, interaction_storage)
            await inter.response.send_message("Эта кнопка не предназначена для вас. (Если вы администратор, перезапустите команду)", ephemeral=True)

    @commands.Cog.listener("on_dropdown")
    async def dropdown_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ["welcomechannelselect"]:
            return
        
        if inter.user.id in interaction_storage and inter.message.id in interaction_storage[inter.user.id]:
            if inter.component.custom_id == "welcomechannelselect":
                selected_value = inter.values[0]
                try:
                    add_to_welcome_json("channel_id", int(selected_value))
                    await inter.response.send_message("Канал был перевыбран", ephemeral=True)
                    await inter.message.edit(embeds=[settingsWelcomeEmbed()])
                except Exception as ex:
                    await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)
        else:
            print(inter.id in interaction_storage, inter.message.id, inter.user.id, interaction_storage)
            await inter.response.send_message("Эта кнопка не предназначена для вас. (Если вы администратор, перезапустите команду)", ephemeral=True)
    

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member):
        if get_welcome_value("off") == False:
            channel = self.bot.get_channel(get_welcome_value("channel_id"))
            footers = ["🔗 discord.gg/cmt-minecraft", "🎮 play.cmt-minecraft.ru"]
            footer_rng = random.randint(0, len(footers) - 1)
            footer = footers[footer_rng]
            button = None
            if get_welcome_value("button") != "0" and get_welcome_value("button_link") != "0":
                button = disnake.ui.Button(label=get_welcome_value("button"), style=disnake.ButtonStyle.link, url=get_welcome_value("button_link"))
            embed = disnake.Embed(
                title=get_welcome_value("title"),
                description=get_welcome_value("description"),
            )
            embed.set_footer(
                text=footer,
            )
            embed.set_image(url=get_welcome_value("image"))
            if button != None:
                await channel.send(embeds=[embed], content=f"<@{member.id}>", components=[button], ephemeral=True)
            else:
                await channel.send(embeds=[embed], content=f"<@{member.id}>", ephemeral=True)

            

def setup(bot: commands.Bot):
    bot.add_cog(Welcome(bot))