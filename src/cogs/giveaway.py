import datetime
import json
import random

import asyncio
import time

import disnake
from disnake.ext import commands


class GiveawayCreator:
    def new_giveaway(self, giveaway_name: str, giveaway_type: str, start_channel: int, messages_channel: int,
                     message_id: int, end_timestamp: int, word: str = None) -> str:
        current_giveaways = self.get_all_giveaways()

        contain_giveaway = False
        contain_same_channel = False

        for key, value in current_giveaways.items():
            print(key)
            print("DHDH2D")
            if key == giveaway_name:
                print("DH2DHD")
                contain_giveaway = True
                break
            else:
                try:
                    if value["channels"]["message_channel"]:
                        for k1, v1 in current_giveaways:
                            if k1 == key:
                                pass
                            else:
                                if value["channels"]["message_channel"] == v1["channels"]["message_channel"]:
                                    contain_same_channel = True
                                    break
                except:
                    pass

        if contain_giveaway:
            print("DHDHD")
            return "На данный момент, уже есть непрошедший розыгрыш с таким именем."
        elif contain_same_channel:
            return ("На данный момент, в таком канале уже проводится выборка сообщений. Попробуйте позже или выберите "
                    "другой канал.")

        general_data = {"giveaway_type": giveaway_type}

        channels = {"start_channel": start_channel}
        if messages_channel is not None:
            channels["messages_channel"] = messages_channel
        general_data["channels"] = channels

        data = {"message_id": message_id, "end_timestamp": end_timestamp}
        if giveaway_type == "word_guesser":
            data["word"] = word
        general_data["data"] = data

        participants = dict()
        general_data["participants"] = participants

        general_data["finished"] = False

        with open(f"./src/data/giveaway.json", "r", encoding="utf-8") as f:
            c_data = json.load(f)
            print(c_data)
            c_data[giveaway_name] = general_data

        with open(f"./src/data/giveaway.json", "w", encoding="utf-8") as f:
            json.dump(c_data, f)

        return "👍"

    def add_msg(self, user_id: int, giveaway_name: str) -> bool:
        with open(f"./src/data/giveaway.json", "r", encoding="utf-8") as f:
            c_data = json.load(f)
            try:
                giveaway = c_data[giveaway_name]
                print(giveaway)
                participants = giveaway["participants"]
                print(participants)
                has_user = False
                for key, _ in participants.items():
                    if key == str(user_id):
                        has_user = True
                        break
                if has_user:
                    participants[str(user_id)] += 1
                else:
                    participants[str(user_id)] = 1
            except Exception:
                return False

        with open(f"./data/giveaway.json", "w", encoding="utf-8") as f:
            json.dump(c_data, f)

        return True

    def set_participant(self, user_id: int, giveaway_name: str) -> bool:
        with open(f"./data/giveaway.json", "r", encoding="utf-8") as f:
            c_data = json.load(f)
            try:
                giveaway = c_data[giveaway_name]
                participants = giveaway["participants"]
                has_user = False
                for key, _ in participants.items():
                    if key == str(user_id):
                        has_user = True
                        break
                if has_user:
                    del participants[str(user_id)]
                else:
                    participants[str(user_id)] = False
            except Exception:
                return False

        with open(f"./data/giveaway.json", "w", encoding="utf-8") as f:
            json.dump(c_data, f)

        return True

    async def finish_giveaway(self, giveaway_name: str, giveaway_message: disnake.Message):
        try:
            with open(f"./data/giveaway.json", "r", encoding="utf-8") as f:
                c_data = json.load(f)
                print(c_data)
                giveaway = c_data[giveaway_name]
                print(giveaway)
                if giveaway["giveaway_type"] == "random":
                    await giveaway_message.edit(components=[
                        disnake.ui.Button(label="", style=disnake.ButtonStyle.red, custom_id=f"join_giveaway",
                                          emoji="🎉", disabled=True),
                        disnake.ui.Button(label="Участники", style=disnake.ButtonStyle.gray,
                                          custom_id=f"get_giveaway_users", disabled=True)])
                giveaway["finished"] = True
        except Exception:
            return "Розыгрыша с таким именем нет"

        with open(f"./data/giveaway.json", "w", encoding="utf-8") as f:
            json.dump(c_data, f)

        return "👍 Готово."

    def get_all_giveaways(self) -> dict:
        giveaway_list = {}
        with open(f"./src/data/giveaway.json", "r", encoding="utf-8") as f:
            c_data = json.load(f)
            try:
                for key, value in c_data.items():
                    print("FUCK NIGGERS")
                    if not value["finished"]:
                        print("FU111CK NIGGERS")
                        giveaway_list[key] = value
                return giveaway_list
            except Exception:
                return {}

    def get_giveaway_by_name(self, giveaway_name: str, check_finish: bool = True) -> dict:
        with open(f"./src/data/giveaway.json", "r", encoding="utf-8") as f:
            c_data = json.load(f)
            giveaway = "there is no giveaway like that"
            try:
                for key, value in c_data.items():
                    print("NIGGER")
                    if key == giveaway_name:
                        print("DHDH")
                        if check_finish is True and c_data[giveaway_name]["finished"] is True:
                            print("GO FUCK YOUSERLF")
                            pass
                        else:
                            print("YEAH HERE IT IS")
                            giveaway = c_data[key]
                            return giveaway
                return giveaway
            except Exception as ex:
                print(ex)
                return "there is no giveaway like that"

    def get_giveaway_by_msg_id(self, message_id: int):
        with open(f"./src/data/giveaway.json", "r", encoding="utf-8") as f:
            c_data = json.load(f)
            giveaway = "there is no giveaway like that"
            try:
                for key, value in c_data.items():
                    if value["data"]["message_id"] == message_id:
                        return key, c_data[key]

                return giveaway
            except Exception:
                return "there is no giveaway like that"


giveaways = GiveawayCreator()


class Giveaways(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channels = list()

    @commands.slash_command(name="giveaway")
    @commands.default_member_permissions(administrator=True)
    async def giveaway(self, inter):
        pass

    @giveaway.sub_command(name="message")
    async def start_message_giveaway(self, inter: disnake.ApplicationCommandInteraction, name: str,
                                     channel: disnake.TextChannel, end_time: int, prize: str, sponsor_link: str = None,
                                     sponsor: disnake.Member = None, text: str = None,
                                     additional_query: str = None):
        """
        Начать роызыгрыш на актив (В определённом канале)

        Parameters
        ----------
        name: Имя розыгрыша (нужно для обработки розыгрыша в будущем)
        channel: Канал, в котором будет проводиться розыгрыш на актив
        end_time: Время до окончания розыгрыша в секундах
        prize: Приз, который получит пользователь
        sponsor_link: Ссылка на сервер спонсора
        sponsor: Спонсор
        text: Текст, который будет написан в сообщении до эмбеда
        additional_query: Дополнительное условие к розыгрышу
        """

        self.channels.append(channel.id)

        description = f'Напиши больше всех сообщений, и выиграй **{prize}**! \n \n'

        description += "✨ **Условия:** ✨\n"
        if sponsor_link is not None:
            description += f"> • 💌 Зайти на **сервер** [спонсора]({sponsor_link}) \n"
        if additional_query is not None:
            description += f"> • 🩵 {additional_query} \n"
        description += f"> • ❤️ Нажать **на сердечко ниже!**\n \n"

        if sponsor_link is not None:
            description += f"\n**💫 Сервер спонсора** • {sponsor_link} 💫 \n"
            if text is not None:
                text += f" • {sponsor_link}"
            else:
                text = sponsor_link

        description += f"\n> 🎉 **Имя розыгрыша:** ``{name}``"
        description += f"\n> 🥳 **Организатор:** <@{inter.user.id}>"
        description += f"\n> 🎁 **Приз:** ``{prize}``"
        if sponsor is not None:
            description += f"\n> 🩵 **Спонсор:** <@{sponsor.id}>"
        description += f"\n> ⌛ **Окончание:** <t:{round(datetime.datetime.now().timestamp() + end_time)}:R>"

        embed = disnake.Embed(
            title='Розыгрыш на активность',
            description=description,
            color=disnake.Color.red()
        )
        embed.set_footer(text=f'©️ Mithic Vanilla. All rights reserved.')

        giveaway_message = await inter.channel.send(content=text, embed=embed)
        await giveaway_message.add_reaction('❤️')

        listing = giveaways.new_giveaway(name, "message", inter.channel.id, channel.id, giveaway_message.id,
                                         round(datetime.datetime.now().timestamp() + end_time))
        if listing != "👍":
            await giveaway_message.delete()
            await inter.response.send_message(listing, ephemeral=True)
            return
        await inter.response.send_message("👍 Готово", ephemeral=True)

        await asyncio.sleep(end_time)

        giveaway = giveaways.get_giveaway_by_name(name)
        if giveaway["finished"] is not True:
            print(giveaway)
            participants = giveaway["participants"]
            await giveaways.finish_giveaway(name, giveaway_message)

            print(participants)
            if len(participants) >= 1:
                winner_id = max(participants, key=lambda i: int(i))
                winner = await self.bot.fetch_user(int(winner_id))
                await giveaway_message.reply(f'Поздравляю, {winner.mention}! Ты выиграл **{prize}**!')
            else:
                await giveaway_message.reply(f'Розыгрыш закончен, но похоже, что никто не участвовал...')

    @giveaway.sub_command(name="random")
    async def start_random_giveaway(self, inter: disnake.ApplicationCommandInteraction, name: str, end_time: int,
                                    prize: str, sponsor_link: str = None, sponsor: disnake.Member = None,
                                    text: str = None, additional_query: str = None):
        """
        Начать розыгрыш с рандом победителем

        Parameters
        ----------
        name: Имя розыгрыша (нужно для обработки розыгрыша в будущем)
        end_time: Время до окончания розыгрыша в секундах
        prize: Приз, который получит пользователь
        sponsor_link: Ссылка на сервер спонсора
        sponsor: Спонсор
        text: Текст, который будет написан в сообщении до эмбеда
        additional_query: Дополнительное условие к розыгрышу
        """

        description = f'Выиграть может каждый! \n \n'

        description += "✨ **Условия:** ✨\n"
        if sponsor_link is not None:
            description += f"> • 💌 Зайти на **сервер** [спонсора]({sponsor_link}) \n"
        if additional_query is not None:
            description += f"> • 🩵 {additional_query} \n"
        description += f"> • 🎉  Нажать **на кнопку ниже!**\n \n"

        if sponsor_link is not None:
            description += f"\n**💫 Сервер спонсора** • {sponsor_link} 💫 \n"
            if text is not None:
                text += f" • {sponsor_link}"
            else:
                text = sponsor_link

        description += f"\n> 🎉 **Имя розыгрыша:** ``{name}``"
        description += f"\n> 🥳 **Организатор:** <@{inter.user.id}>"
        description += f"\n> 🎁 **Приз:** ``{prize}``"
        if sponsor is not None:
            description += f"\n> 🩵 **Спонсор:** <@{sponsor.id}>"
        description += f"\n> ⌛ **Окончание:** <t:{round(datetime.datetime.now().timestamp() + end_time)}:R>"

        embed = disnake.Embed(
            title=name,
            description=description,
            color=disnake.Color.red()
        )
        embed.set_footer(text=f'©️ Mithic Vanilla. All rights reserved.')

        giveaway_message = await inter.channel.send(embed=embed, content=text, components=[
            disnake.ui.Button(label="", style=disnake.ButtonStyle.red, custom_id=f"join_giveaway",
                              emoji="🎉"),
            disnake.ui.Button(label="Участники", style=disnake.ButtonStyle.gray, custom_id=f"get_giveaway_users")])

        listing = giveaways.new_giveaway(giveaway_name=name, giveaway_type="random", start_channel=inter.channel.id,
                                         messages_channel=None, message_id=giveaway_message.id,
                                         end_timestamp=round(datetime.datetime.now().timestamp() + end_time))
        if listing != "👍":
            await giveaway_message.delete()
            await inter.response.send_message(listing, ephemeral=True)
            return
        await inter.response.send_message("👍")

        await asyncio.sleep(end_time)

        giveaway = giveaways.get_giveaway_by_name(name)
        print(giveaway)
        if giveaway["finished"] is not True:
            participants = giveaway["participants"]
            await giveaways.finish_giveaway(name, giveaway_message)

            users = []

            for key, _ in participants.items():
                users.append(key)

            if len(participants) >= 1:
                winner_id = random.choice(users)
                winner = await self.bot.fetch_user(int(winner_id))
                await giveaway_message.reply(f'Поздравляю, {winner.mention}! Ты выиграл **{prize}**!')
            else:
                await giveaway_message.reply(f'Розыгрыш закончен, но похоже, что никто не участвовал...')

    @giveaway.sub_command(name="word_guesser")
    async def start_word_giveaway(self, inter: disnake.ApplicationCommandInteraction, name: str, word: str,
                                  channel: disnake.TextChannel,
                                  prize: str, hint: str, sponsor_link: str = None, sponsor: disnake.Member = None,
                                  text: str = None, additional_query: str = None):
        """
        Начать конкурс "Угадай слово"

        Parameters
        ----------
        name: Имя розыгрыша (нужно для обработки розыгрыша в будущем)
        word: Слово, которое нужно угадать
        channel: Канал, в котором нужно угадать слово
        prize: Приз, который получит пользователь
        hint: Подсказка к слову
        sponsor_link: Ссылка на сервер спонсора
        sponsor: Спонсор
        text: Текст, который будет написан в сообщении до эмбеда
        additional_query: Дополнительное условие к розыгрышу
        """

        self.channels.append(channel.id)

        description = f'Угадай слово, и выиграй **{prize}**! \n \n'

        description += "✨ **Условия:** ✨\n"
        if sponsor_link is not None:
            description += f"> • 💌 Зайти на **сервер** [спонсора]({sponsor_link}) \n"
        if additional_query is not None:
            description += f"> • 🩵 {additional_query} \n"
        description += f"> • ❤️  Нажать ** на сердечко ниже!**\n \n"

        if sponsor_link is not None:
            description += f"\n**💫 Сервер спонсора** • {sponsor_link} 💫 \n"
            if text is not None:
                text += f" • {sponsor_link}"
            else:
                text = sponsor_link

        if hint is not None:
            description += f"\n> ❔ **Подсказка:** ``{hint}`` \n"

        description += f"\n> 🎉 **Имя розыгрыша:** ``{name}``"
        description += f"\n> 🥳 **Организатор:** <@{inter.user.id}>"
        description += f"\n> 🎁 **Приз:** ``{prize}``"
        if sponsor is not None:
            description += f"\n> 🩵 **Спонсор:** <@{sponsor.id}>"
        description += f"\n> ⌛ **Окончание:** ``пока слово не будет угадано``"

        embed = disnake.Embed(
            title="Угадай слово",
            description=description,
            color=disnake.Color.red()
        )
        embed.set_footer(text=f'©️ Mithic Vanilla. All rights reserved.')

        giveaway_message = await inter.channel.send(embed=embed, content=text)

        await giveaway_message.add_reaction('❤️')

        listing = giveaways.new_giveaway(giveaway_name=name, giveaway_type="word_guesser", start_channel=inter.channel.id,
                                         messages_channel=channel.id, message_id=giveaway_message.id,
                                         end_timestamp=None, word=word)
        if listing != "👍":
            await giveaway_message.delete()
            await inter.response.send_message(listing, ephemeral=True)
            return
        await inter.response.send_message("👍 Готово", ephemeral=True)

    @giveaway.sub_command(name="stop")
    async def finish(self, inter: disnake.ApplicationCommandInteraction, name: str):
        """
        Остановить розыгрыш (не дав выиграть кому-либо)

        Parameters
        ----------
        name: Имя розыгрыша
        """
        giveaway_message = await inter.channel.fetch_message(
            giveaways.get_giveaway_by_name(giveaway_name=name)["data"]["message_id"])
        response = await giveaways.finish_giveaway(name, giveaway_message)

        await inter.response.send_message(response, ephemeral=True)

    @giveaway.sub_command(name="reroll")
    async def reroll(self, inter: disnake.ApplicationCommandInteraction, name: str):
        """
        Зарероллить розыгрыш (после окончания/остановки)

        Parameters
        ----------
        name: Имя розыгрыша
        """
        giveaway = giveaways.get_giveaway_by_name(name, False)
        print(giveaway)

        if giveaway != "there is no giveaway like that":
            if giveaway["finished"] is True:
                giveaway_message = await inter.channel.fetch_message(giveaway["data"]["message_id"])
                participants = giveaway["participants"]

                users = []

                for key, _ in participants:
                    users.append(key)

                if len(participants) >= 1:
                    winner_id = random.choice(users)
                    winner = await self.bot.fetch_user(int(winner_id))
                    await giveaway_message.reply(f'Розыгрыш зарероллен. Поздравляю, {winner.mention}! Вы выиграли!')
                else:
                    await giveaway_message.reply(f'Розыгрыш зарероллен, но похоже, что никто не участвовал...')

                await inter.response.send_message("👍 Готово.", ephemeral=True)
            else:
                await inter.response.send_message("Розыгрыш по такому имени ещё не закончен!", ephemeral=True)
        else:
            await inter.response.send_message("Розыгрыша с таким именем не найдено.", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if not message.author.bot:
            ex_giveaways = giveaways.get_all_giveaways()
            print("DHHDHDHD111")
            print(len(ex_giveaways))
            if len(ex_giveaways) >= 1:
                print("GO FUCK YOURSELF SHIT")
                channelid = message.channel.id
                if channelid in self.channels:
                    print("GO FUCK YOURSELF22 SHIT")
                    name = ""
                    for key, value in ex_giveaways.items():
                        print("GO FUCK1 YOURSELF SHIT")
                        if value["channels"]["messages_channel"] == message.channel.id:
                            name = key
                            print("NIGGA")
                    current_giveaway = giveaways.get_giveaway_by_name(name)
                    if current_giveaway["giveaway_type"] == "message":
                        print("GO FUCK YOURSELF SH111111IT")
                        giveaway_message = await message.channel.fetch_message(current_giveaway["data"]["message_id"])
                        reactions = giveaway_message.reactions
                        reacted_users = []
                        for reaction in reactions:
                            async for user in reaction.users():
                                reacted_users.append(user.id)
                        if message.author.id in reacted_users:
                            print("GO FUCK YOU222323RSELF SHIT")
                            giveaways.add_msg(message.author.id, name)
                    elif current_giveaway["giveaway_type"] == "word_guesser":
                        print("GO FUCK YOURSELF SH111111IT")
                        if current_giveaway["data"]["word"] == message.content:
                            needed_channel_id = current_giveaway["channels"]["start_channel"]
                            needed_channel = self.bot.get_channel(needed_channel_id)
                            giveaway_message = await needed_channel.fetch_message(current_giveaway["data"]["message_id"])
                            participants = current_giveaway["participants"]
                            await giveaways.finish_giveaway(name, giveaway_message)

                            users = []

                            for key, _ in participants.items():
                                users.append(key)

                            winner = message.author
                            await giveaway_message.reply(
                                f'Поздравляю, {winner.mention}! Ты выиграл!')
                            await message.reply(
                                f'Поздравляю, {winner.mention}! Ты выиграл!')

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == "join_giveaway":
            func = giveaways.get_giveaway_by_msg_id(inter.message.id)
            name = func[0]
            giveaway = func[1]

            has_user = False
            for key, _ in giveaway["participants"].items():
                if key == str(inter.user.id):
                    has_user = True
                    break
            if has_user:
                await inter.response.send_message("Вы были убраны из розыгрыша", ephemeral=True)
            else:
                await inter.response.send_message("Вы были добавлены в розыгрыш", ephemeral=True)
            giveaways.set_participant(inter.user.id, name)
        elif inter.component.custom_id == "get_giveaway_users":
            func = giveaways.get_giveaway_by_msg_id(inter.message.id)
            giveaway_data = func[1]["participants"]

            await inter.response.send_message(f"Всего участников: **{len(giveaway_data)}**", ephemeral=True)
        elif inter.component.custom_id == "get_my_chance":
            func = giveaways.get_giveaway_by_msg_id(inter.message.id)
            giveaway_data = func[1]["participants"]
            leng = len(giveaway_data)
            if str(inter.user.id) in giveaway_data:
                await inter.response.send_message(f"Ваш шанс: **123**", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Giveaways(bot))
