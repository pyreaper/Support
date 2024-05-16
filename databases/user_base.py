# бд для работы с юзерами. экономика и юзеры - тут

import random
import sqlite3
from datetime import datetime

import disnake
import hashlib


# Transfer errors
class TransferErrors(Exception):
    pass


# Has no money
class HasNoMoneyException(TransferErrors):
    """Exception raised for user's money error

    Attributes:
        transfer_hash -- hash of the invalid transaction
        message -- explanation of the error
    """

    def __init__(self, transfer_hash: str, message="Selected user has no money that was excepted"):
        self.transfer_hash = transfer_hash
        self.message = message
        super().__init__(self.message)


# Transactions with the same hash exception
class SameHashException(TransferErrors):
    """Exception raised for same hashes in 2 transactions

    Attributes:
        transfer_hash -- hash of the invalid transaction
        message -- explanation of the error
    """

    def __init__(self, transfer_hash: str, message="Other transaction has the same hash"):
        self.transfer_hash = transfer_hash
        self.message = message
        super().__init__(self.message)


# Something went wrong exception
class SomethingWentWrongException(TransferErrors):
    """Exception raised for unknown errors

    Parameters:
        transfer_hash -- hash of the invalid transaction
        message -- explanation of the error
        exception_data -- data of the exception
    """

    def __init__(self, transfer_hash: str, exception_data, message="Unknown error was handled"):
        self.transfer_hash = transfer_hash
        self.message = message
        self.exception_data = exception_data
        super().__init__(self.message)


class Database:
    def __init__(self, guild: disnake.Guild, bot):
        """
        Запуск бд с добавлением таблиц (если не существуют)

        :param guild: Гилд
        """
        self.bot = bot

        # Устанавливаем соединение с базой данных
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            username TEXT NOT NULL,
            level INTEGER,
            level_points INTEGER,
            next_level_points INTEGER
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Cards (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            card_number INTEGER,
            end_date TEXT NOT NULL,
            cvv TEXT NOT NULL,
            money INTEGER,
            getTransfers INTEGER,
            type TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ShopItems (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price INTEGER,
            role_id INTEGER,
            command TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transfers (
            id INTEGER PRIMARY KEY,
            sender_card INTEGER,
            receiver_card INTEGER,
            sender_id INTEGER,
            receiver_id INTEGER,
            reason TEXT NOT NULL,
            bonus_amount INTEGER,
            transfer_hash TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Server (
            id INTEGER PRIMARY KEY,
            money INTEGER,
            shop_commission INTEGER,
            transfer_commission INTEGER,
            voucher_commission INTEGER,
            server_bonus_commission INTEGER,
            a_shop_commission INTEGER,
            a_transfer_commission INTEGER
            )
        ''')

        # Applications

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Applications (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            give_role INTEGER,
            description TEXT NOT NULL,
            emoji TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Questions (
            id INTEGER PRIMARY KEY,
            question TEXT NOT NULL,
            application_connection_id INTEGER,
            type TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Commands (
            id INTEGER PRIMARY KEY,
            command TEXT NOT NULL,
            application_connection_id INTEGER
            )
        ''')

        connection.commit()

        cursor.execute('SELECT * FROM Users')
        users = cursor.fetchall()
        print(users)

        for member in guild.members:
            if type(self.get_user_ex(member.id)) is SomethingWentWrongException and not member.bot:
                self.new_user(user_id=member.id, username=member.name, level=0, level_points=0, next_level_points=100)

        connection.close()

    @staticmethod
    def generate_unique_hash(data: str):
        """
        Генерация уникального набора символов путём хеширования

        :parameter data: Айди сообщения
        """
        number_str_encoded = data.encode('utf-8')

        # Create a hashlib object using SHA-256
        hash_object = hashlib.sha256(number_str_encoded)

        # Get the hexadecimal digest of the hash
        hex_digest = hash_object.hexdigest()

        # Take the first 5 characters of the hexadecimal digest as the hash
        hashed_value = hex_digest[:5]

        return hashed_value

    # Shop items
    @staticmethod
    def new_shop_item(name, price, role_id, *commands):
        """
        Создание нового предмета в магазине

        :parameter name: Имя предмета
        :parameter price: Цена предмета
        :parameter role_id: Айди выдаваемой роли
        :parameter commands: Команды
        """
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()
        commands_list = ""
        count = 0
        for command in commands:
            count += 1
            commands_list += f"{command}"
            if len(commands) != count:
                commands_list += "::"
        cursor.execute('INSERT INTO ShopItems (name, price, role_id, command) VALUES (?, ?, ?, ?)',
                       (name, price, role_id, commands_list))

        connection.commit()
        connection.close()

    @staticmethod
    def delete_shop_item(name):
        """
        Удаление предмета из магазина

        :parameter name: Имя предмета
        """
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        try:
            cursor.execute('DELETE FROM ShopItems WHERE name = ?', (name,))
        except Exception:
            return 0

        connection.commit()
        connection.close()

    @staticmethod
    def get_all_items():
        """
        :return: Возвращает все объекты из магазина
        """
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('SELECT name, price, role_id, command FROM ShopItems ORDER BY price ASC')
        items = cursor.fetchall()

        return items

    async def give_item(self, inter: disnake.ApplicationCommandInteraction, user_id: int, item: tuple):
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        response = await self.bot.get_slash_command("minecraft rcon").callback(inter=inter, command=item[3],
                                                                               logneed=False)
        return response

    # User
    @staticmethod
    def new_user(user_id, username, level, level_points, next_level_points):
        """
        Создание нового пользователя

        :parameter user_id: Айди пользователя
        :parameter username: Имя пользователя
        :parameter level: Начальный уровень
        :parameter level_points: Поинты уровня
        :parameter next_level_points: Поинты до следующего уровня
        """

        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('INSERT INTO Users (user_id, username, level, level_points, next_level_points) VALUES '
                       '(?, ?, ?, ?, ?)',
                       (user_id, username, level, level_points, next_level_points))

        connection.commit()
        connection.close()

    @staticmethod
    def get_user_ex(user_id):
        """
        Поиск пользователя по айди

        :parameter user_id: Айди пользователя
        :returns: Возвращает пользователя или ошибку
        """
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('SELECT user_id, username FROM Users WHERE user_id = ?', (user_id,))
        data = cursor.fetchone()
        connection.close()

        if data is None:
            return SomethingWentWrongException(None,
                                               exception_data=[user_id],
                                               message="Can't find user with the arguments presented")
        return data

    # Cards
    @staticmethod
    def new_card(user_id, card_type: str = "debit"):
        """
        Открытие карты

        :parameter user_id: Айди пользователя
        :parameter card_type: Тип карты (временно не используется, всегда debit)
        """
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        random1 = random.randint(1111, 9999)
        random2 = random.randint(1111, 9999)
        random3 = random.randint(1111, 9999)
        card_number = f"3279 {random1} {random2} {random3}"

        random4 = random.randint(111, 999)
        cvv = f"{random4}"

        expiration_date = round(datetime.now().timestamp() + (31536000 * 10))

        cursor.execute('INSERT INTO Cards (user_id, card_number, end_date, cvv, money, getTransfers, type) VALUES '
                       '(?, ?, ?, ?, ?, ?, ?)',
                       (user_id, card_number, expiration_date, cvv, 0, 0, card_type))
        connection.commit()
        connection.close()

    @staticmethod
    def get_user_money(user_id, card_type: str = "debit"):
        """
        Получение данных о деньгах на карте

        :parameter user_id: Айди пользователя
        :parameter card_type: Тип карты (временно не используется, всегда debit)
        :returns: Возвращает список (айди юзера и деньги) или ошибку
        """
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()
        print(user_id, card_type)

        cursor.execute('SELECT user_id, money FROM Cards WHERE user_id = ? AND type = ?', (user_id, card_type))
        money = cursor.fetchone()
        connection.close()
        if money is None:
            return SomethingWentWrongException(None,
                                               exception_data=[user_id, card_type],
                                               message="Can't find user money with the arguments presented")
        return money

    @staticmethod
    def get_card_data(user_id, card_type: str = "debit"):
        """
        Получение данных о карте

        :parameter user_id: Айди пользователя
        :parameter card_type: Тип карты (временно не используется, всегда debit)
        :returns: Возвращает карту или ошибку
        """
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('SELECT user_id, card_number, end_date, cvv, type FROM Cards WHERE user_id = ? AND type = ?',
                       (user_id, card_type))
        card = cursor.fetchone()
        connection.close()
        if card is None:
            return SomethingWentWrongException(None,
                                               exception_data=[user_id, card_type],
                                               message="Can't find card with the arguments presented")
        return card

    @staticmethod
    def get_transfer_access(user_id, card_type: str = "debit"):
        """
        Получение данных о включенных переводах на карте

        :parameter user_id: Айди пользователя
        :parameter card_type: Тип карты (временно не используется, всегда debit)
        :returns: Возвращает список (айди юзера и данные по карте) или ошибку
        """

        if card_type == "anonymous":
            return user_id, 1, "anonymous"

        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('SELECT user_id, getTransfers, type FROM Cards WHERE user_id = ? AND type = ?',
                       (user_id, card_type))
        access = cursor.fetchone()
        connection.close()
        if access is None:
            return SomethingWentWrongException(None,
                                               exception_data=[user_id, card_type],
                                               message="Can't find transaction access with the arguments presented")
        return access

    @staticmethod
    def set_transfer_access(user_id, value: int = 0, card_type: str = "debit"):
        """
        Установка возможности переводов на карту

        :parameter user_id: Айди пользователя
        :parameter value: Значение на установку (0 выключены, 1 включены)
        :parameter card_type: Тип карты (временно не используется, всегда debit)
        """
        if card_type == "anonymous":
            return
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('UPDATE Cards SET getTransfers = ? WHERE user_id = ? AND type = ?', (value, user_id, card_type))

        connection.commit()
        connection.close()

    @staticmethod
    def set_money(user_id, money, card_type: str = "debit"):
        """
        Установка денег на карте

        :parameter user_id: Айди пользователя
        :parameter money: Значение на установку
        :parameter card_type: Тип карты (временно не используется, всегда debit)
        """
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('UPDATE Cards SET money = ? WHERE user_id = ? AND type = ?', (money, user_id, card_type))

        connection.commit()
        connection.close()

    def decrease_money(self, user_id, much, card_type: str = "debit"):
        """
        Установка денег на карте

        :parameter user_id: Айди пользователя
        :parameter much: Значение на установку (-)
        :parameter card_type: Тип карты (временно не используется, всегда debit)
        :returns: Чаще всего None, может вернуть ошибку
        """
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        user_money = self.get_user_money(user_id)[1] - much
        if user_money < 0:
            connection.close()
            return SomethingWentWrongException(None,
                                               exception_data=[user_id, much, card_type],
                                               message="User's balance is smaller than the argument")

        cursor.execute('UPDATE Cards SET money = ? WHERE user_id = ? AND type = ?', (user_money, user_id, card_type))

        connection.commit()
        connection.close()

    def increase_money(self, user_id, much, card_type: str = "debit"):
        """
        Установка денег на карте

        :parameter user_id: Айди пользователя
        :parameter much: Значение на установку (+)
        :parameter card_type: Тип карты (временно не используется, всегда debit)
        :returns: Чаще всего None, может вернуть ошибку
        """
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        user_money = self.get_user_money(user_id)[1] + much

        cursor.execute('UPDATE Cards SET money = ? WHERE user_id = ? AND type = ?', (user_money, user_id, card_type))

        connection.commit()
        connection.close()

    # Transfers

    def transfer_money(self, sender_card, receiver_card, sender_id, receiver_id, reason, bonus_amount, transfer_hash):
        """
        Перевод средств с карты на карту


        :parameter sender_card: Карта отправляющего
        :param receiver_card: Карта получающего
        :param sender_id: Айди отправляющего
        :param receiver_id: Айди получающего
        :param reason: Причина перевода
        :param bonus_amount: Количество средств на перевод
        :param transfer_hash: Хеш транзакции

        :returns: Данные о переводе и ответ на уменьшение денег (ошибку или None)
        """
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        decrease_response = self.decrease_money(sender_id, bonus_amount)
        if decrease_response == SomethingWentWrongException:
            return decrease_response

        self.increase_money(receiver_id, bonus_amount)

        cursor.execute('INSERT INTO Transfers (sender_card, receiver_card, sender_id, receiver_id, reason, '
                       'bonus_amount, transfer_hash) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (sender_card, receiver_card, sender_id, receiver_id, reason, bonus_amount, transfer_hash))
        connection.commit()
        cursor.execute('SELECT id, sender_card, receiver_card, sender_id, receiver_id, reason, '
                       'bonus_amount, transfer_hash FROM Transfers WHERE transfer_hash = ?',
                       (transfer_hash,))
        transfer_data = cursor.fetchone()

        connection.close()

        return transfer_data, decrease_response

    @staticmethod
    def transfer_an_money(sender_card, receiver_card, sender_id, receiver_id, bonus_amount, transfer_msg_id):
        # Soon...
        """
        global sender_type, receiver_type
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()
        if sender_card[:4] == 3279 and receiver_card[:4] == 8888:
            sender_type = "debit"
            receiver_type = "anonymous"
        elif sender_card[:4] == 8888 and receiver_card[:4] == 3279:
            sender_type = "anonymous"
            receiver_type = "debit"
        elif sender_card[:4] == 8888 and receiver_card[:4] == 8888:
            sender_type = "anonymous"
            receiver_type = "anonymous"

        transfer_hash = self.generate_unique_hash(str(transfer_msg_id))

        response = self.decrease_money(sender_card, bonus_amount, sender_type)
        self.increase_money(receiver_card, bonus_amount, receiver_type)

        cursor.execute('INSERT INTO Transfers (sender_card, receiver_card, sender_id, receiver_id, reason, '
                       'bonus_amount, transfer_hash) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (sender_card, receiver_card, sender_id, receiver_id, "Анонимный перевод", bonus_amount,
                        transfer_hash))

        connection.commit()
        connection.close()

        return response
        """

        return "soon"

    @staticmethod
    def get_transfer_info(transfer_id: int = None, transfer_hash: str = None):
        """
        Информация о переводе
        Можно указать 1 значение, другое оставив пустым. В приоритете хеш транзакции

        :parameter transfer_id: Айди трансфера
        :param transfer_hash: Хеш транзакции

        :returns: Данные о переводе или ошибку
        """
        if transfer_hash is not None:
            transfer_find_data = ["transfer_hash", transfer_hash]
        elif transfer_id is not None:
            transfer_find_data = ["id", transfer_id]
        else:
            return SomethingWentWrongException(transfer_hash,
                                               exception_data="Both arguments were not presented in get_transfer_data",
                                               message="Argument handling error")

        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('SELECT sender_card, receiver_card, sender_id, receiver_id, reason, bonus_amount FROM '
                       'Transfers WHERE ? = ?', (transfer_find_data[0], transfer_find_data[1]))
        transfer = cursor.fetchone()
        connection.close()
        if transfer is None:
            return SomethingWentWrongException(transfer_hash,
                                               exception_data=transfer_find_data,
                                               message="Can't find transfer with presented parameters")

        return transfer

    # Levels

    @staticmethod
    def get_user_level(user_id):
        """
        Получение уровня пользователя


        :parameter user_id: Айди пользователя

        :returns: Список (айди, уровень, поинты, поинты до следующего уровня) или ошибку
        """
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()
        print(user_id)

        cursor.execute('SELECT user_id, level, level_points, next_level_points FROM '
                       'Users WHERE user_id = ?', (user_id,))
        level = cursor.fetchone()
        if level is None:
            return SomethingWentWrongException(None,
                                               exception_data=[user_id],
                                               message="Can't find user's level with the arguments presented")

        connection.close()

        return level

    def add_level_points(self, user_id, amount):
        """
        Добавить поинты уровня


        :parameter user_id: Айди пользователя
        :parameter amount: Количество на выдачу

        :returns: Код 100 если поинты были добавлены или список с кодом 200 и данными о добавлении
        """
        global response
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        pr_level_data = self.get_user_level(user_id)
        print(pr_level_data, "djdhdjdjjdjdj")
        pr_level_points = pr_level_data[2]

        cursor.execute('UPDATE Users SET level_points = ? WHERE user_id = ?', (amount + pr_level_points, user_id))
        connection.commit()

        level_data = self.get_user_level(user_id)
        level = level_data[1]
        print(level)
        level_points = level_data[2]
        next_level_points = level_data[3]

        print(user_id, amount)

        if level_data[2] >= level_data[3]:
            cursor.execute(
                'UPDATE Users SET level_points = ?, level = ?, next_level_points = ? WHERE user_id = ?',
                (level_points - next_level_points, level + 1, next_level_points + (25 * int(level / 5) + 25), user_id)
            )
            connection.commit()

            n_level_data = self.get_user_level(user_id)

            return 200, n_level_data[1]

        connection.close()
        return [100]

    @staticmethod
    def set_user_level(user_id, amount):
        """
        Добавление уровня пользователю


        :parameter user_id: Айди пользователя
        :parameter amount: Количество на выдачу
        """
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('UPDATE Users SET level = ? WHERE user_id = ?', (amount, user_id))
        connection.commit()
        connection.close()
