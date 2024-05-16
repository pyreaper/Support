# бд для работы с заявками. её трогать не нужно, заявки ещё не делались

import sqlite3

import disnake


# Something went wrong exception

class SomethingWentWrongException(Exception):
    """Exception raised for unknown errors

    Attributes:
        message -- explanation of the error
        exception_data -- data of the exception
    """

    def __init__(self, exception_data, message="Unknown error was handled"):
        self.message = message
        self.exception_data = exception_data
        super().__init__(self.message)


class Database:
    def __init__(self, bot):
        """
        Запуск бд с добавлением таблиц (если не существуют)

        Attributes:
            bot -- объект бота
        """
        self.bot = bot

        # Устанавливаем соединение с базой данных
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        # Applications

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Applications (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            give_role INTEGER,
            channel_id INTEGER,
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

        connection.close()

    # Applications
    @staticmethod
    def new_application(name: str, give_role: int, channel_id: int,
                        description: str, emoji: str):
        """
        Запуск бд с добавлением таблиц (если не существуют)

        Attributes:
            bot -- объект бота
        """
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM Applications WHERE name = ?',
                       (name,))
        appl = cursor.fetchone()
        if appl is not None:
            return SomethingWentWrongException(exception_data=[name, give_role,
                                                               description, emoji],
                                               message="Two names (applications) are equal")

        cursor.execute('INSERT INTO Applications VALUES (?, ?, ?, ?, ?)',
                       (name, give_role, channel_id, description, emoji))
        connection.commit()
        cursor.execute('SELECT * FROM Applications WHERE name = ?',
                       (name,))
        application_data = cursor.fetchone()

        connection.close()

        return application_data

    @staticmethod
    def get_application_data(name: str = None, application_id: int = None):
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        if name is not None:
            find_data = ["name", name]
            print(find_data, ":XDSIFHSGDGFYSD")
        elif application_id is not None:
            find_data = ["application_id", application_id]
        else:
            return SomethingWentWrongException(exception_data=[name, application_id],
                                               message="Two arguments are None (applications)")

        cursor.execute(f'SELECT * FROM '
                       f'Applications WHERE {find_data[0]} = ?', (find_data[1],))
        application = cursor.fetchone()
        print(application)
        if application is None:
            return SomethingWentWrongException(exception_data=find_data,
                                               message="Can't find application with the arguments presented")

        connection.close()

        return application

    # Questions
    @staticmethod
    def new_question(question: str, application_connect_id: int, question_type: str):
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM Questions WHERE question = ?',
                       (question,))
        question_ex = cursor.fetchone()
        if question_ex is not None:
            return SomethingWentWrongException(exception_data=[question, application_connect_id, type],
                                               message="Two names (questions) are equal")

        cursor.execute('INSERT INTO Questions VALUES (?, ?, ?)',
                       (question, application_connect_id, question_type))
        connection.commit()
        cursor.execute('SELECT * FROM Questions WHERE question = ?',
                       (question,))
        question_data = cursor.fetchone()

        connection.close()

        return question_data

    @staticmethod
    def get_question_data(question: str = None, application_connect_id: int = None):
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        if question is not None:
            find_data = ["question", question]
        elif application_connect_id is not None:
            find_data = ["application_connect_id", application_connect_id]
        else:
            return SomethingWentWrongException(exception_data=[question, application_connect_id],
                                               message="Two arguments are None (questions)")

        cursor.execute(f'SELECT * FROM Questions WHERE {find_data[0]} = ?',
                       (find_data[1],))
        question_data = cursor.fetchall()
        if question_data is None or question_data == ():
            return SomethingWentWrongException(exception_data=find_data,
                                               message="Can't find question with the arguments presented")

        connection.close()

        return question_data

    @staticmethod
    def new_command(command: str, application_connect_id: int):
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM Commands WHERE command = ?',
                       (command,))
        command_ex = cursor.fetchone()
        if command_ex is not None:
            return SomethingWentWrongException(exception_data=[command, application_connect_id],
                                               message="Two names (commands) are equal")

        cursor.execute('INSERT INTO Commands VALUES (?, ?)',
                       (command, application_connect_id, type))
        connection.commit()
        cursor.execute('SELECT * FROM Commands WHERE command = ?',
                       (command,))
        command_data = cursor.fetchone()

        connection.close()

        return command_data

    @staticmethod
    def get_command_data(command: str = None, application_connect_id: int = None):
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        if command is not None:
            find_data = ["question", command]
        elif application_connect_id is not None:
            find_data = ["application_connect_id", application_connect_id]
        else:
            return SomethingWentWrongException(exception_data=[command, application_connect_id],
                                               message="Two arguments are None (questions)")

        cursor.execute(f'SELECT * FROM Commands WHERE {find_data[0]} = ?',
                       (find_data[1],))
        command_data = cursor.fetchall()
        if command_data is None or command_data == ():
            return SomethingWentWrongException(exception_data=find_data,
                                               message="Can't find question with the arguments presented")

        connection.close()

        return command_data

    @staticmethod
    def get_all_applications():
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM Applications')
        applications = cursor.fetchall()

        connection.close()

        return applications

    @staticmethod
    def edit_application_data(key: str, value: str, name: str):
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute(f'UPDATE Applications SET {key} = ? WHERE name = ?', (value, name))

        connection.commit()
        connection.close()

    @staticmethod
    def delete_application(name: str):
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('DELETE FROM Applications WHERE name = ?', (name,))

        connection.commit()
        connection.close()

    @staticmethod
    def delete_question(question: str):
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('DELETE FROM Questions WHERE question = ?', (question,))

        connection.commit()
        connection.close()

    @staticmethod
    def delete_command(command: str):
        connection = sqlite3.connect('123.db')
        cursor = connection.cursor()

        cursor.execute('DELETE FROM Commands WHERE command = ?', (command,))

        connection.commit()
        connection.close()
