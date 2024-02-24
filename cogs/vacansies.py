import json
import random

import disnake
from disnake import TextInputStyle
from disnake.ext import commands

def add_to_vacansies_json(key, value):
    with open("./data/vacansies.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        c_data[key] = value

    with open("./data/vacansies.json", "w", encoding="utf-8") as f:
        json.dump(c_data, f)


def get_vacansies_value(key):
    with open("./data/vacansies.json", "r", encoding="utf-8") as f:
        c_data = json.load(f)
        return c_data[key]

def check_nickname(nickname):
    for i in nickname:
        if not i.isalnum():
            if not i == "_":
                return 0
        else:
            if any(letter in set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя") for letter in i.lower()):
                return 0
    
    return 1

senders = {}
interaction_storage = {}

def updateEmbed():
    embed = disnake.Embed(
        title="Настройки вакансий",
        description=f"**Титул:** ``{get_vacansies_value('title')}`` \n **Описание: \n** ```{get_vacansies_value('description')}``` \n **Канал для отправки:** <#{str(get_vacansies_value('channel_id'))}> \n **Канал для заявок:** <#{str(get_vacansies_value('sender_channel_id'))}> \n **Картинка:** ``ниже в сообщении`` \n \n **Если вы хотите закрыть вакансию, оставьте в поле названия 0 (без пробелов и других символов) и переотправьте сообщение**"
    )
    embed.set_image(url=get_vacansies_value("image"))
    return embed

class VacansiesSettingsModal(disnake.ui.Modal):
    def __init__(self, findex: str):
        self.findex = findex

        components = [
            disnake.ui.TextInput(
                label="Название вакансии",
                value=get_vacansies_value(findex)[0],
                custom_id="name",
                style=TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Вопрос 1",
                value=get_vacansies_value(findex)[1],
                custom_id="question1",
                style=TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Вопрос 2",
                value=get_vacansies_value(findex)[2],
                custom_id="question2",
                style=TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Вопрос 3",
                value=get_vacansies_value(findex)[3],
                custom_id="question3",
                style=TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Вопрос 4",
                placeholder="...",
                value=get_vacansies_value(findex)[4],
                custom_id="question4",
                style=TextInputStyle.short,
                required=False,
            ),
        ]
        super().__init__(title="Настройки", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        builder = []
        keycounter = 0

        for key, value in inter.text_values.items():
            print(key, value)
            print(keycounter)
            if value != '':
                print("ALTT22AL")
                builder.append(value)
            else:
                print("ALTTAL")
                builder.append(get_vacansies_value(self.findex)[keycounter])
            keycounter += 1
            print(builder)

        add_to_vacansies_json(self.findex, builder)

        await inter.message.edit(embeds=[updateEmbed()])
        await inter.response.send_message("Настройки были успешно изменены. Если вы меняли имена должностей, нажмите на кнопку для переотправки сообщения", ephemeral=True)


class VEmbedSettingsModal(disnake.ui.Modal):
    def __init__(self):
        print("HI")
        print(get_vacansies_value("title"), get_vacansies_value("description"))
        components = [
            disnake.ui.TextInput(
                label="Титул",
                value=get_vacansies_value("title"),
                custom_id="title",
                style=TextInputStyle.short,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Описание",
                value=get_vacansies_value("description"),
                custom_id="description",
                style=TextInputStyle.paragraph,
                required=False,
            ),
            disnake.ui.TextInput(
                label="Ссылка на картинку",
                placeholder="...",
                value=get_vacansies_value("image"),
                custom_id="image",
                style=TextInputStyle.short,
                required=False,
            ),
        ]
        print("HUI")
        super().__init__(title="Настройки", components=components)
        print("HUI")

    async def callback(self, inter: disnake.ModalInteraction):
        for key, value in inter.text_values.items():
            print("HUI")
            if value != '':
                if key == "numbersincaptcha":
                    add_to_vacansies_json(key, int(value))
                else:
                    add_to_vacansies_json(key, value)

        await inter.message.edit(embeds=[updateEmbed()])
        await inter.response.send_message("Настройки были успешно изменены. Нажмите на кнопку для переотправки сообщения.", ephemeral=True)

async def vac_builder(name: str, questions: dict, user: disnake.Member, findex: str):
    channel = user.guild.get_channel(get_vacansies_value("sender_channel_id"))
    if channel:
        embed = disnake.Embed(
            title=f"Вакансия от {user.nick or user.name} на {name}"
        )
        print(questions)
        for key, value in questions.items():
            question = get_vacansies_value(findex)[int(key)]
            embed.add_field(name=f'#**{question}**', value=value, inline=False)

        await channel.send(embeds=[embed])

class VacansiesModal(disnake.ui.Modal):
    def __init__(self, findex: str, user_id: int):
        self.findex = findex
        self.user_id = user_id
        senders[user_id] = str(random.randint(1111, 9999))

        components = [
            disnake.ui.TextInput(
                label=get_vacansies_value(findex)[1],
                custom_id="1",
                style=TextInputStyle.paragraph,
                required=True,
                max_length=500,
            ),
            disnake.ui.TextInput(
                label=get_vacansies_value(findex)[2],
                custom_id="2",
                style=TextInputStyle.paragraph,
                required=True,
                max_length=500,
            ),
            disnake.ui.TextInput(
                label=get_vacansies_value(findex)[3],
                custom_id="3",
                style=TextInputStyle.paragraph,
                required=True,
                max_length=500,
            ),
            disnake.ui.TextInput(
                label=get_vacansies_value(findex)[4],
                custom_id="4",
                style=TextInputStyle.paragraph,
                required=True,
                max_length=500,
            ),
            disnake.ui.TextInput(
                label="Капча",
                custom_id="captcha",
                placeholder=senders[self.user_id],
                style=TextInputStyle.short,
                required=True,
                max_length=4,
                min_length=4,
            ),
        ]
        super().__init__(title=f"{get_vacansies_value(findex)[0]}", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        if inter.text_values["captcha"] == senders[self.user_id]:
            del inter.text_values["captcha"]
            await vac_builder(name=get_vacansies_value(self.findex)[0], questions=inter.text_values, user=inter.user, findex=self.findex)
            await inter.response.send_message("Ваша заявка была отправлена модераторам на проверку. Вам напишут, если вашей заявкой заинтересуются.", ephemeral=True)
        else:
            await inter.response.send_message("Капча решена неверно", ephemeral=True)

async def button_builder(findex: str):
    print(get_vacansies_value(findex)[0])
    if get_vacansies_value(findex)[0] != "0":
        button = disnake.ui.Button(label=get_vacansies_value(findex)[0], style=disnake.ButtonStyle.gray, custom_id=f"vacansies_{findex}")
        return button
    else:
        return "0"

async def build_vacansies_embed(inter: disnake.MessageInteraction):
    print("AAKKA")
    keycount = 0
    buttons = [await button_builder("first"), await button_builder("second"), await button_builder("thrid")]
    print(buttons)
    for i in buttons:
        print(i, keycount)
        print("AHAHHA")
        if type(i) != disnake.ui.Button:
            buttons.pop(keycount)
        keycount += 1
    print("DJHDDJDJDJDJ")
    print(buttons)
    embed = disnake.Embed(
        title=get_vacansies_value("title"),
        description=get_vacansies_value("description")
    )
    print("DJHDDJDJDJDJ")
    embed.set_image(url=get_vacansies_value("image"))
    print("DJHDDJDJDJDJ")
    sended_msg = await inter.send(embeds=[embed], components=buttons)
    print("DJHDDJDJDJDJ")
    return sended_msg.id

class Vacansies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="vacansies_settings", description="Настройки вакансий", dm_permission=False)
    @commands.default_member_permissions(administrator=True)
    async def vacsettings(self, inter: disnake.ApplicationCommandInteraction):
        print(interaction_storage)
        await inter.response.send_message("Эмбед с настройками успешно отправлен", ephemeral=True)
        msg = await inter.channel.send(embeds=[updateEmbed()], components=[disnake.ui.ChannelSelect(custom_id="vacansieschannelselect", placeholder="Канал"), disnake.ui.ChannelSelect(custom_id="vacsenderchannelselect", placeholder="Канал (туда пойдут заявки)"), disnake.ui.Button(label="Изменить настройки эмбеда", style=disnake.ButtonStyle.gray, custom_id="changevacansiessettings"), disnake.ui.Button(label="Отправить сообщение в канал", style=disnake.ButtonStyle.success, custom_id="sendvacansiesmessage"), disnake.ui.Button(label="Удалить сообщение из канала", style=disnake.ButtonStyle.danger, custom_id="deletevacansiesmessage"), disnake.ui.Button(label="Изменить настройки первой вакансии", style=disnake.ButtonStyle.primary, custom_id="changevacansiesfirst"), disnake.ui.Button(label="Изменить настройки второй вакансии", style=disnake.ButtonStyle.primary, custom_id="changevacansiessecond"), disnake.ui.Button(label="Изменить настройки третьей вакансии", style=disnake.ButtonStyle.primary, custom_id="changevacansiesthrid")])
        print(msg)
        if inter.user.id not in interaction_storage:
            interaction_storage[inter.author.id] = [msg.id]
        else:
            interaction_storage[inter.author.id].append(msg.id)

    @commands.Cog.listener("on_button_click")
    async def button_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ["changevacansiessettings", "sendvacansiesmessage", "deletevacansiesmessage", "changevacansiesfirst", "changevacansiessecond", "changevacansiesthrid", "vacansies_first", "vacansies_second", "vacansies_thrid"]:
            return
        if inter.user.id in interaction_storage and inter.message.id in interaction_storage[inter.user.id]:
            if inter.component.custom_id == "changevacansiessettings":
                await inter.response.send_modal(modal=VEmbedSettingsModal())
            elif inter.component.custom_id == "sendvacansiesmessage":
                try:
                    print("DJDDJDJ")
                    if get_vacansies_value("vacansies_msg_id") != 0:
                        print("DJDDJDJ")
                        channel = inter.guild.get_channel(get_vacansies_value("channel_id"))
                        print("DJDDJDJ")
                        msg = await channel.fetch_message(get_vacansies_value("vacansies_msg_id"))
                        await msg.delete()
                        print("DJDDJDJ")
                        add_to_vacansies_json("vacansies_msg_id", 0)
                    sendedmsgid = await build_vacansies_embed(inter.guild.get_channel(get_vacansies_value("channel_id")))
                    await inter.response.send_message("Успешно", ephemeral=True)
                    add_to_vacansies_json("vacansies_msg_id", sendedmsgid)
                except Exception as ex:
                    #add_to_vacansies_json("vacansies_msg_id", 0)
                    await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Айди сообщения было сброшено (удалите предыдущее если таковое имеется сами). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)
            
            elif inter.component.custom_id == "deletevacansiesmessage":
                try:
                    if get_vacansies_value("vacansies_msg_id") != 0:
                        channel = inter.guild.get_channel(get_vacansies_value("channel_id"))
                        msg = await channel.fetch_message(get_vacansies_value("vacansies_msg_id"))
                        await msg.delete()
                        add_to_vacansies_json("vacansies_msg_id", 0)
                        await inter.response.send_message("Успешно", ephemeral=True)
                    else:
                        await inter.response.send_message("Похоже, сообщение ещё не было отправлено. Отправьте его", ephemeral=True)
                except Exception as ex:
                    #add_to_vacansies_json("vacansies_msg_id", 0)
                    await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Айди сообщения было сброшено (удалите предыдущее если таковое имеется сами). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)
            elif inter.component.custom_id == "changevacansiesfirst":
                await inter.response.send_modal(modal=VacansiesSettingsModal("first"))
            elif inter.component.custom_id == "changevacansiessecond":
                await inter.response.send_modal(modal=VacansiesSettingsModal("second"))
            elif inter.component.custom_id == "changevacansiesthrid":
                await inter.response.send_modal(modal=VacansiesSettingsModal("thrid"))
            elif inter.component.custom_id == "vacansies_first":
                await inter.response.send_modal(modal=VacansiesModal("first", inter.user.id))
            elif inter.component.custom_id == "vacansies_second":
                await inter.response.send_modal(modal=VacansiesModal("second", inter.user.id))
            elif inter.component.custom_id == "vacansies_thrid":
                await inter.response.send_modal(modal=VacansiesModal("thrid", inter.user.id))
        else:
            print(inter.id in interaction_storage, inter.message.id, inter.user.id, interaction_storage)
            await inter.response.send_message("Эта кнопка не предназначена для вас. (Если вы администратор, перезапустите команду)", ephemeral=True)


    @commands.Cog.listener("on_dropdown")
    async def dropdown_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ["vacansieschannelselect", "vacsenderchannelselect"]:
            return
        if inter.user.id in interaction_storage and inter.message.id in interaction_storage[inter.user.id]:
            if inter.component.custom_id == "vacansieschannelselect":
                selected_value = inter.values[0]
                try:
                    if get_vacansies_value("vacansies_msg_id") != 0:
                        channel = inter.guild.get_channel(get_vacansies_value("channel_id"))
                        msg = await channel.fetch_message(get_vacansies_value("vacansies_msg_id"))
                        await msg.delete()
                        add_to_vacansies_json("vacansies_msg_id", 0)
                    add_to_vacansies_json("channel_id", int(selected_value))
                    await inter.response.send_message("Канал был перевыбран", ephemeral=True)
                    await inter.message.edit(embeds=[updateEmbed()])
                except Exception as ex:
                    #add_to_vacansies_json("vacansies_msg_id", 0)
                    await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Айди сообщения было сброшено (удалите предыдущее если таковое имеется сами). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)
            elif inter.component.custom_id == "vacsenderchannelselect":
                selected_value = inter.values[0]
                try:
                    if get_vacansies_value("vacansies_msg_id") != 0:
                        channel = inter.guild.get_channel(get_vacansies_value("sender_channel_id"))
                        msg = await channel.fetch_message(get_vacansies_value("vacansies_msg_id"))
                        await msg.delete()
                        add_to_vacansies_json("vacansies_msg_id", 0)
                    add_to_vacansies_json("sender_channel_id", int(selected_value))
                    await inter.response.send_message("Канал был перевыбран", ephemeral=True)
                    await inter.message.edit(embeds=[updateEmbed()])
                except Exception as ex:
                    #add_to_vacansies_json("vacansies_msg_id", 0)
                    await inter.response.send_message(f"Произошла ошибка (код: ``{ex}``). Айди сообщения было сброшено (удалите предыдущее если таковое имеется сами). Попробуйте снова. \nПри повторении ошибки обратитесь к `_thecoffee_`.", ephemeral=True)
        else:
            print(inter.id in interaction_storage, inter.user.id, interaction_storage)
            await inter.response.send_message("Эта кнопка не предназначена для вас. (Если вы администратор, перезапустите команду)", ephemeral=True)
            

def setup(bot: commands.Bot):
    bot.add_cog(Vacansies(bot))