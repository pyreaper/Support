import asyncio
import random

import disnake
from disnake.ext import commands
from databases import user_base

from random_unicode_emoji import random_emoji

embed_users = {}

transfer_facts_list = [
    "> **Каждая транзакция зашифрованна с помощью хешей транзакции.** \n",
    "> **Хеш транзакции - ключ, который даёт доступ к передаче информации, "
    "без которого транзакцию совершить невозможно.** \n",
    "> **Каждый хеш уникален. Они записываются в базу, доступ к которой есть только"
    "у администраторов.**",

    "> **Время обработки транзакции зависит от нагрузки на сервер,"
    "а так же от количества входящих данных на обработку.**",

    "> **Пользователь имеет право потребовать возврат средств, "
    "если на это есть весомая причина.**",

    "> **С любовью, разработчики Mithic Vanilla ❤️‍🩹 (ты нашёл пасхалку)**",

    "> **У сервера есть свой трейлер, посмотрите его!**",

    "> **На стадии первичной обработки, сервер шифрует данные как эмодзи**"
]


class CardSelectDropdown(disnake.ui.StringSelect):
    def __init__(self, db: user_base.Database, user_id: int):
        # Define the options that will be displayed inside the dropdown.
        # You may not have more than 25 options.
        # There is a `value` keyword that is being omitted, which is useful if
        # you wish to display a label to the user, but handle a different value
        # here within the code, like an index number or database id.

        cards = [db.get_card_data(user_id), db.get_card_data(user_id, "anonymous")]
        counter = 0
        cards_data = {}
        for card in cards:
            if type(card) != user_base.SomethingWentWrongException:
                counter += 1
                card_data = {"label": f"Карта {counter}"}
                if card[4] == "debit":
                    card_type = "Дебетовая карта"
                    emoji = "💳"
                else:
                    card_type = "Анонимная карта"
                    emoji = "🔒"
                card_data["description"] = card_type
                card_data["emoji"] = emoji
                cards_data[card[4]] = card_data

        options = []
        for key, value in cards_data.items():
            options.append(
                disnake.SelectOption(
                    label=value["label"],
                    description=value["description"],
                    emoji=value["emoji"]
                )
            )

        # We will include a placeholder that will be shown until an option has been selected.
        # The min and max values indicate the minimum and maximum number of options to be selected -
        # in this example we will only allow one option to be selected.
        super().__init__(
            placeholder="Выберите карту",
            min_values=1,
            max_values=1,
            options=options,
        )

    # This callback is called each time a user has selected an option
    async def callback(self, inter: disnake.MessageInteraction):
        db = user_base.Database(inter.user.guild, inter.bot)
        card = self.values[0]

        data_to_send = inter.message.embeds[0]

        sender_field = data_to_send.fields[0]
        sender_id = sender_field.value.replace("<", "")
        sender_id = sender_id.replace(">", "")
        sender_id = sender_id.replace("@", "")
        sender_id = int(sender_id)
        sender_card_data = db.get_card_data(sender_id)

        receiver_field = data_to_send.fields[1]
        receiver_id = receiver_field.value.replace("<", "")
        receiver_id = receiver_id.replace(">", "")
        receiver_id = receiver_id.replace("@", "")
        receiver_id = int(receiver_id)
        receiver_card_data = db.get_card_data(receiver_id)

        bonus_field = data_to_send.fields[2]
        bonus_amount = int(bonus_field.value)

        reason_field = data_to_send.fields[3]
        reason = reason_field.value

        transfer_hash = db.generate_unique_hash(str(inter.message.id))
        if type(db.get_transfer_info(transfer_hash=transfer_hash)) != user_base.SomethingWentWrongException:
            await inter.response.send_message("Транзакция с таким хешем уже происходила. "
                                              "Попробуйте создать новую /transfer)", ephemeral=True)
            return
        print(sender_card_data[1], receiver_card_data[1],
                                          sender_id, receiver_id,
                                          reason, bonus_amount, transfer_hash)
        transfer_data = db.transfer_money(sender_card_data[1], receiver_card_data[1],
                                          sender_id, receiver_id,
                                          reason, bonus_amount, transfer_hash)
        if type(transfer_data) == user_base.SomethingWentWrongException:
            await inter.response.send_message("Похоже, что-то пошло не так.", ephemeral=True)
            return
        else:
            description = "**⌛ Подтверждаем транзакцию в базе. Это может занять некоторое время...**\n\n"
            description += "**Интересный факт:**\n"
            description += random.choice(transfer_facts_list)
            embed = disnake.Embed(
                title="Подтверждение транзакции",
                description=description,
                color=disnake.Color.green(),
            )

            await inter.response.send_message("Транзакция была отправлена в обработку", ephemeral=True)

            msg = await inter.channel.send(embed=embed, content=f"<@{sender_id}> <@{receiver_id}>")
            await asyncio.sleep(random.randint(1, 3) / 10)
            await msg.edit(content=f"**Статус обработки: Запись данных в базу...** \n ``Путь: user_base.py/transfer ("
                                   f"exec arguments: {random_emoji(count=4)}``")
            await asyncio.sleep(random.randint(1, 3) / 10)
            await msg.edit(content="**Статус обработки: Шифрование данных в базе...** \n ``Путь: user_base.py/transfer ("
                                   f"exec arguments: {random_emoji(count=4)}``")
            await asyncio.sleep(random.randint(1, 3) / 10)
            await msg.edit(content="**Статус обработки: Проверка записанных данных...** \n ``Путь: user_base.py/transfer ("
                                   f"exec arguments: {random_emoji(count=4)}``")
            await asyncio.sleep(random.randint(2, 4))

            new_description = "**Транзакция была успешно завершена!**"
            new_embed = disnake.Embed(
                title="Транзакция завершена",
                description=new_description,
                color=disnake.Color.green(),
            )

            new_embed.add_field(name="⏩ Отправитель", value=f"<@{sender_id}>", inline=False)
            new_embed.add_field(name="⏩ Получатель", value=f"<@{receiver_id}>", inline=False)
            new_embed.add_field(name="💵 Сумма", value=f"{bonus_amount}", inline=False)
            new_embed.add_field(name="❔ Причина", value=f"**{reason}**", inline=False)

            await msg.edit(embed=new_embed, content="")


class TransferView(disnake.ui.View):
    def __init__(self, db: user_base.Database, user_id: int):
        # You would pass a new `timeout=` if you wish to alter it, but
        # we will leave it empty for this example so that it uses the default 180s.
        super().__init__()

        # Now let's add the `StringSelect` object we created above to this view
        self.add_item(CardSelectDropdown(db, user_id))


class DBTEST(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="profile",
                            dm_permission=False)
    async def info(self, inter: disnake.ApplicationCommandInteraction):
        global components
        description = "**Для получения информации, выберите нужную категорию:** \n\n> 💳 **- Основная информация**\n> " \
                      "🤝 **- Открытие переводов**\n> 🛒 **- Информация по переводам** ``(временно недоступно)``\n\n"
        db = user_base.Database(inter.user.guild, self.bot)

        if type(db.get_card_data(inter.user.id)) != user_base.SomethingWentWrongException:
            components = [
                disnake.ui.Button(label="", style=disnake.ButtonStyle.green, emoji="💳", custom_id="user_card_info"),
                disnake.ui.Button(label="", style=disnake.ButtonStyle.green, emoji="🤝", custom_id="transfer_open"),
                disnake.ui.Button(label="", style=disnake.ButtonStyle.green, emoji="🛒", custom_id="transfer_info",
                                  disabled=True)
            ]
        else:
            components = [
                disnake.ui.Button(label="", style=disnake.ButtonStyle.green, emoji="💳", custom_id="user_card_info"),
                disnake.ui.Button(label="", style=disnake.ButtonStyle.green, emoji="🤝", custom_id="transfer_open",
                                  disabled=True),
                disnake.ui.Button(label="", style=disnake.ButtonStyle.green, emoji="🛒", custom_id="transfer_info",
                                  disabled=True)
            ]
            description += ("```Просьба обратить внимание, что у вас нет карты - для получения информации по ней, "
                            "нужно её открыть. \n"
                            "Для продолжения, нажмите на первую кнопку.```")

        embed = disnake.Embed(
            title="Информация по карте",
            description=description,
            color=disnake.Color.green()
        )

        await inter.response.send_message(embed=embed, components=components, ephemeral=True)

    @commands.slash_command(name="setmoney",
                            dm_permission=False)
    @commands.default_member_permissions(administrator=True)
    async def setmoney(self, inter: disnake.ApplicationCommandInteraction, count: int, user: disnake.Member = None):
        db = user_base.Database(guild=inter.guild, bot=self.bot)
        if user is None:
            user = inter.user

        description = f"**👍 Бонусы были успешно отправлены пользователю {user.mention}**"
        color = disnake.Color.green()

        embed = disnake.Embed(
            title="Отправка бонусов",
            description=description,
            color=color,
        )
        embed.set_author(name="Mithic Vanilla",
                         icon_url="https://cdn.discordapp.com/attachments/1105911982873378816/1222136596174733382/image.png?ex=662f7c66&is=662e2ae6&hm=75c38008d297e0716f21b73a0fd46346a85d417b37f5e10cf6d05caf17f88d04&")

        db.set_money(money=count, user_id=user.id)
        await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.slash_command(name="new_item",
                            dm_permission=False)
    @commands.default_member_permissions(administrator=True)
    async def new_item(self, inter: disnake.ApplicationCommandInteraction, name: str, price: int, role: disnake.Role,
                       command: str):
        db = user_base.Database(guild=inter.guild, bot=self.bot)

        db.new_shop_item(name=name, price=price, role_id=role.id, command=command)

        description = f"**👍 Предмет был добавлен в магазин**"
        color = disnake.Color.green()

        embed = disnake.Embed(
            title="Добавление предмета в магазин",
            description=description,
            color=color,
        )
        embed.set_author(name="Mithic Vanilla",
                         icon_url="https://cdn.discordapp.com/attachments/1105911982873378816/1222136596174733382/image.png?ex=662f7c66&is=662e2ae6&hm=75c38008d297e0716f21b73a0fd46346a85d417b37f5e10cf6d05caf17f88d04&")

        await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.slash_command(name="delete_item",
                            dm_permission=False)
    @commands.default_member_permissions(administrator=True)
    async def delete_item(self, inter: disnake.ApplicationCommandInteraction, name: str, price: int, role: disnake.Role,
                          command: str):
        db = user_base.Database(guild=inter.guild, bot=self.bot)

        response = db.delete_shop_item(name=name)
        if response is None:
            description = f"👍 Предмет был удалён из магазин"
            color = disnake.Color.green()

            embed = disnake.Embed(
                title="Удаление предмета из магазина",
                description=description,
                color=color,
            )

            embed.set_author(name="Mithic Vanilla",
                             icon_url="https://cdn.discordapp.com/attachments/1105911982873378816/1222136596174733382/image.png?ex=662f7c66&is=662e2ae6&hm=75c38008d297e0716f21b73a0fd46346a85d417b37f5e10cf6d05caf17f88d04&")

            await inter.response.send_message(embed=embed, ephemeral=True)
        else:
            description = f"❌ Что-то пошло не так."
            color = disnake.Color.red()

            embed = disnake.Embed(
                title="Удаление предмета из магазина",
                description=description,
                color=color,
            )

            embed.set_author(name="Mithic Vanilla",
                             icon_url="https://cdn.discordapp.com/attachments/1105911982873378816/1222136596174733382"
                                      "/image.png?ex=662f7c66&is=662e2ae6&hm"
                                      "=75c38008d297e0716f21b73a0fd46346a85d417b37f5e10cf6d05caf17f88d04&")

            await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.slash_command(name="shop_items",
                            dm_permission=False)
    async def shop_items(self, inter: disnake.ApplicationCommandInteraction):
        db = user_base.Database(guild=inter.guild, bot=self.bot)

        items = db.get_all_items()

        description = ""
        count = 0
        for item in items:
            count += 1
            description += f"> **{count}. {item[0]} <@&{item[2]}> -** ``{item[1]}``"

        color = disnake.Color.green()

        embed = disnake.Embed(
            title="Предметы",
            description=description,
            color=color,
        )
        embed.set_author(name="Mithic Vanilla",
                         icon_url="https://cdn.discordapp.com/attachments/1105911982873378816/1222136596174733382/image.png?ex=662f7c66&is=662e2ae6&hm=75c38008d297e0716f21b73a0fd46346a85d417b37f5e10cf6d05caf17f88d04&")

        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="buy_item",
                            dm_permission=False)
    async def buy_item(self, inter: disnake.ApplicationCommandInteraction, item_id: int):
        db = user_base.Database(guild=inter.guild, bot=self.bot)

        items = db.get_all_items()

        if len(items) >= item_id:
            item = items[item_id - 1]
            print(item, items)
            price = item[1]
            print(price)
            if price <= db.get_user_money(inter.user.id)[1]:
                item_role = disnake.utils.get(inter.guild.roles, id=item[2])
                has_role = False
                for role in inter.user.roles:
                    if role == item_role:
                        has_role = True
                        break

                if not has_role:
                    db.decrease_money(user_id=inter.user.id, much=item[1])
                    #await db.give_item(inter=inter, user_id=inter.user.id, item=item)
                    await inter.user.add_roles(item_role, reason="Покупка роли")
                    await inter.response.send_message("Товар был успешно приобретён", ephemeral=True)
                else:
                    await inter.response.send_message("Вы уже приобретали этот товар ранее",
                                                      ephemeral=True)
            else:
                await inter.response.send_message("У вас недостаточно средств для покупки этого товара!",
                                                  ephemeral=True)
        else:
            await inter.response.send_message("Похоже, что вы ввели неверный айди товара", ephemeral=True)

    @commands.slash_command(name="transfer",
                            dm_permission=False)
    async def transfer(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member, amount: int,
                       reason: str = "Не указана"):
        db = user_base.Database(guild=inter.guild, bot=self.bot)

        if inter.user != user and not user.bot:
            print(db.get_card_data(inter.user.id))
            print(db.get_card_data(user.id))
            if type(db.get_card_data(inter.user.id)) != user_base.SomethingWentWrongException and type(
                    db.get_card_data(user.id)) != user_base.SomethingWentWrongException:
                if db.get_transfer_access(inter.user.id)[1] == 1 and db.get_transfer_access(user.id)[1] == 1:
                    if db.get_user_money(inter.user.id)[1] >= amount:
                        embed = disnake.Embed(
                            title="Подтвердите перевод",
                            description="**Проверьте данные и примите решение. \nВозврат транзакции невозможен без "
                                        "уважительной причины!**",
                            color=disnake.Color.green()
                        )
                        embed.add_field(name="⏩ Отправитель", value=f"{inter.user.mention}", inline=False)
                        embed.add_field(name="⏩ Получатель", value=f"{user.mention}", inline=False)
                        embed.add_field(name="💵 Сумма", value=f"{amount}", inline=False)
                        embed.add_field(name="❔ Причина", value=f"**{reason}**", inline=False)

                        view = TransferView(db, inter.user.id)
                        await inter.response.send_message(embed=embed, ephemeral=True, view=view)
                    else:
                        await inter.response.send_message("Операция отменена. Причина: недостаточно средств.",
                                                          ephemeral=True)
                else:
                    await inter.response.send_message(
                        "У одного из участников операции выключены переводы. Проверьте и попробуйте снова.",
                        ephemeral=True)
            else:
                await inter.response.send_message("Неверная карта для перевода.", ephemeral=True)
        else:
            await inter.response.send_message(
                "Неверный участник для перевода.", ephemeral=True)

    @commands.Cog.listener("on_button_click")
    async def button_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ["user_card_info", "transfer_open", "transfer_info", "open_card"]:
            return

        if inter.message.id in embed_users:
            if (embed_users[inter.message.id] != inter.user.id and inter.component.custom_id != "startcaptcha"
                    or inter.component.custom_id != "sendcaptcha"):
                await inter.response.send_message("Эта кнопка не принадлежит вам.", ephemeral=True)

        if inter.component.custom_id == "user_card_info":
            db = user_base.Database(guild=inter.guild, bot=self.bot)

            if not type(db.get_card_data(inter.user.id)) == user_base.SomethingWentWrongException:
                embed = disnake.Embed(
                    title="Информация по карте пользователя",
                    color=disnake.Color.green()
                )

                card_data = db.get_card_data(inter.user.id)

                embed.add_field(name="💳 Номер карты", value=str(card_data[1]), inline=False)
                embed.add_field(name="⌛ Дата окончания", value=str(card_data[2]), inline=False)
                embed.add_field(name="🔐 CVV", value=f"||{str(card_data[3])}||", inline=False)
                embed.add_field(name="👁️ Держатель карты", value=f"{inter.user.mention}", inline=False)
                embed.add_field(name="💰 Баланс", value=f"``{db.get_user_money(inter.user.id)[1]}``", inline=False)

                await inter.response.send_message(embed=embed, ephemeral=True)
            else:
                if db.get_user_level(inter.user.id)[1] >= 15:
                    embed = disnake.Embed(
                        title="Карта отсутствует",
                        description="**У вас отсутствует дебетовая карта. Для открытия, нажмите на кнопку ниже** \n"
                                    "\n 💳 **Карта даёт вам эти преймущества:**"
                                    "\n> - **Возможность получать и переводить деньги**"
                                    "\n> - **Возможность покупать товары в магазине**"
                                    "\n> - **Возможность оплачивать покупки на маркетплейсе переводом бонусов**",
                        color=disnake.Color.green()
                    )

                    await inter.response.send_message(embed=embed, ephemeral=True, components=[
                        disnake.ui.Button(label="Открыть карту", style=disnake.ButtonStyle.green, custom_id="open_card")
                    ])
                else:
                    embed = disnake.Embed(
                        title="Карта отсутствует",
                        description="**У вас отсутствует дебетовая карта. Для открытия необходим 15 уровень!** \n"
                                    "\n 💳 **Карта даёт вам эти преймущества:**"
                                    "\n> - **Возможность получать и переводить деньги**"
                                    "\n> - **Возможность покупать товары в магазине**"
                                    "\n> - **Возможность оплачивать покупки на маркетплейсе переводом бонусов**",
                        color=disnake.Color.green()
                    )

                    await inter.response.send_message(embed=embed, ephemeral=True, components=[
                        disnake.ui.Button(label="Открыть карту", style=disnake.ButtonStyle.green, custom_id="open_card",
                                          disabled=True)
                    ])
        elif inter.component.custom_id == "open_card":
            db = user_base.Database(guild=inter.guild, bot=self.bot)

            if type(db.get_card_data(inter.user.id)) == user_base.SomethingWentWrongException:
                db.new_card(inter.user.id)
                await inter.response.send_message("Карта была открыта. Проверьте профиль для получения информации.",
                                                  ephemeral=True)
            else:
                await inter.response.send_message("У вас уже есть дебетовая карта!", ephemeral=True)
        elif inter.component.custom_id == "transfer_open":
            db = user_base.Database(guild=inter.guild, bot=self.bot)

            if type(db.get_card_data(inter.user.id)) != user_base.SomethingWentWrongException:
                text = ""

                if db.get_transfer_access(inter.user.id)[1] == 0:
                    db.set_transfer_access(inter.user.id, 1)
                    text = "Переводы успешно включены"
                else:
                    db.set_transfer_access(inter.user.id)
                    text = "Переводы успешно выключены"

                await inter.response.send_message(content=text, ephemeral=True)
            else:
                await inter.response.send_message("У вас нет карты.", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(DBTEST(bot))
