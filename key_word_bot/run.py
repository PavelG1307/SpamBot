import sqlite3
from datetime import date
from pyrogram import Client, idle
from pyrogram.handlers import MessageHandler
from pyrogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from user import User

def connect_db():
    global cursor, connection
    connection = sqlite3.connect("database.db", check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Event(
    date Date,
    project VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL
    )"""
    )
    cursor.execute("""CREATE TABLE IF NOT EXISTS  KeyWord(
    event INT,
    keyword VARCHAR(512) NOT NULL
    )"""
    )
    connection.commit()
    
def handl(client, message):
    global users
    for user in users:
        if user.id == message.chat.id:
            file_name, text = user.get_file(message.text)
            if file_name is not None:
                try:
                    client.send_document(chat_id = message.chat.id, document = file_name, caption=text)
                    message.reply('Чтобы cгенерировать следющий файл, нажмите /add_event')
                except Exception as e:
                    print(e)
                    message.reply(f'Ошибка:\n{e}')
                return
            else:
                message.reply(text)
                return
    users.append(User(id=message.chat.id, mode=None, cursor=cursor, connection=connection))
    message.reply(users[-1].get_file(message.text)[1])
    return


def main():
    global users
    connect_db()
    users=[]
    mybot = Client(
        'bot',
        bot_token='5206831411:AAH3_lnU98drAyS97s-MUfDjr5gYQnyT56E',
        api_id=9696471,
        api_hash='6181f0cc6d734e181c2aec501d691eb9'
    )
    mybot.add_handler(MessageHandler(handl))
    mybot.start()
    idle()
    mybot.stop()

if __name__ == '__main__':
    main()