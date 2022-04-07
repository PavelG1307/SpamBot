import os
from pathlib import Path
import sys
from pyrogram import Client, idle, filters
from pyrogram.handlers import MessageHandler
from pyrogram.errors import RPCError, SessionPasswordNeeded, PeerFlood
import asyncio
from account import Account

def def_sett():
    global id_user_registration, accounts_list, mode_temp, mode_acc
    id_user_registration=0
    accounts_list=[]
    mode_temp=None
    mode_acc=[]


def resource_path(relative):
    return Path(sys.argv[0]).parent/relative

def open_from_file():
    global bot, accounts_list
    session_string = 'BQAYWqi3c2OkiL51OTVDhksaA25Txb4F7csOP_kp-4e18uiPJi7okWoRY2GHcLAoB0WRtZBFuZQWAYm75EAf-Cduzmf09H6cZxEoE85qwY8voqrJLL0cxSMpCC3zvEZPBhIylW2Bmv0v7Wbmyz1OA9AYkgiCZmJbK7-JEdC8qRJxMHygreqDYayNqJufoINtjQy_uTZvrF-kCYd3XXbTfkeJgC1A5IKfzcwcVGV-exzfLc1WqgiaR_hc35cvJAT_VrrktI-te4PFLB2Dp_HCQYBMLfeqGwZZa-vPhsmqIUe1NqPr8Lj9lHR7tSYcAdZtgt2pptJf-UnAV6fAcy7fWiaAAAAAATnyF9EA'
    with open(resource_path('bot_tokken.ini'), 'r', encoding='utf-8') as fp:
        bot = Client('bot', bot_token=fp.read())
    with open(resource_path('accounts.ini'), 'r', encoding='utf-8') as fp:
        data = fp.read()
        for line in data.splitlines():
            accounts_list.append(Account(Client(session_string)))
        print('В работе ' + str(len(accounts_list)) + ' аккаунтов')
    files = os.listdir(Path(sys.argv[0]).parent/'chats')
    for i in range(len(accounts_list)):
        print(files[i])
        with(open(Path(sys.argv[0]).parent/'chats'/files[i], 'r', encoding='utf-8')) as fp:
            data = fp.readlines()
            accounts_list[i].answer_list = data
            print('Всего чатов', len(data))



def Save(t):
    if t == "Client":
        with open(resource_path('bot_tokken.ini'), 'w', encoding='utf-8') as fp:
            for acc in accounts_list:
                fp.write(acc.get_str())

async def success_login(message):
    global id_acc, answer_list, id_user,level_users,stt_reg,mode, id_user_registration, mode_acc
    print("Успешный вход!")
    id_user_registration=0
    mode_acc.append("Null")
    mode=0
    print("Connect")
    await accounts_list[-1].client.disconnect()
    await accounts_list[-1].client.start()
    print(await accounts_list[-1].get_str())
    with open(resource_path('accounts.ini'), 'w', encoding='utf-8') as fp:
            for acc in accounts_list:
                fp.write(await acc.get_str())
    await message.reply("Вход выполнен успешно!")
    # os.execv(sys.executable, ['python'] + sys.argv)

async def bot_handl(client, message):
    global proxyb, proxyc, mode, id_user_registration, code, phonehash, accounts_list, phonenumber, code
    print(message.text)
    if not message.text is None:
        if id_user_registration==message.chat.id:
            if mode==5:
                try:
                    await accounts_list[-1].client.check_password(message.text)
                except RPCError as e:
                    print(e)
                    await message.reply("Ошибка входа! Введите номер телефона аккаунта")
                    id_user_registration=0
                    return
                else:
                    await success_login(message)
                    return
                return

            if mode==4:
                try:
                    code=message.text[1:-1]
                    print(code)
                    await accounts_list[-1].client.sign_in(phone_number=phonenumber,phone_code_hash=phonehash, phone_code=code)
                except SessionPasswordNeeded:
                    await message.reply("Введите пароль аккаунта")
                    mode+=1
                except Exception as e:
                    await message.reply("Ошибка")
                    accounts_list.pop(-1)
                    print(e)
                    mode=0
                    id_user_registration=0
                else: 
                    await success_login(message)
                    mode=0
                    return
                return

            if mode==3:
                if not proxyb:
                    accounts_list.append(Account(Client("account"+str(len(accounts_list)), proxy=None)))
                    print('add')
                    await accounts_list[-1].client.connect()
                phonenumber=message.text
                print("Телефон: " + phonenumber)
                try:
                    phonehash = (await (accounts_list[-1].client.send_code(phonenumber))).phone_code_hash
                except Exception as e:
                    await message.reply("Ошибка")
                    accounts_list.pop(-1)
                    print(e)
                    mode+=1
                    id_user_registration=0
                else:
                    print(accounts_list[-1].client.test_mode) 
                    await message.reply("Введите код в формате 0ХХХХХ0, где ХХХХХ - одноразовый код")
                    mode+=1
                return

            if message.text == "/without_proxy":
                accounts_list.pop(-1)
                proxyb=False
                mode+=1
                return
            
            if message.text=="/try":
                try:
                    await message.reply("Пробую подключиться...")
                    await accounts_list[-1].client.connect()
                except Exception as e:
                    print(e)
                    await message.reply( "Произошла ошибка! Повторить попытку? /try\nЛибо ведите другие hostname и порт\n/without_proxy – подключиться без прокси")
                else:
                    mode+=1
                    await message.reply("Подключение прокси прошло успешно! Введите номер телефона аккаунта:")
                    print(proxyc)
                return

            if mode==2:
                try:
                    if len(message.text.split(" ")) == 2:
                        proxyc = dict(
                            hostname=message.text.split(" ")[0],
                            port=int(message.text.split(" ")[1]),
                            username=None,
                            password=None
                        )
                        accounts_list.append(Account(Client("account"+str(int(accounts_list[-1].session_name[7])+1), proxy=proxyc)))
                        await message.reply("Пробую подключиться...")
                        await accounts_list[-1].client.connect()
                    else:
                        if len(message.text.split(" ")) == 4:
                            proxyc = dict(
                                hostname=message.text.split(" ")[0],
                                port=int(message.text.split(" ")[1]),
                                username=message.text.split(" ")[2],
                                password=message.text.split(" ")[3]
                            )
                            accounts_list.append(Account(Client("account"+str(int(accounts_list[-1].session_name[7])+1), proxy=proxyc)))
                            await message.reply("Пробую подключиться...")
                            await accounts_list[-1].client.connect()
                            
                        else:
                            await message.reply("Невозможно распознать! Начать с начала? /start")
                            return


                except Exception as e:
                    print(e)
                    await message.reply("Произошла ошибка! Повторить попытку? /try\nЛибо ведите другие hostname и порт\n/without_proxy – подключиться без прокси")
                else:
                    mode+=1
                    proxyb=True
                    await message.reply("Подключение прокси прошло успешно! Введите номер телефона аккаунта:")
                    print(proxyc)
                return

            if mode==1:
                if message.text=="/no":
                    proxyc = dict(hostname=None, port=None,
                                username=None, password=None)
                    await message.reply("Введите номер телефона аккаунта")
                    mode+=2
                    proxyb=False
                    return
                if message.text == "/yes":
                    await message.reply("Введите hostname и port через пробел (также возможно ввести username и password)")
                    mode+=1
                    return

            if mode==0 or mode==2 and message.text=="/start":
                mode=1
                await message.reply("Добро пожаловать! Подключить прокси? /yes или /no")
                id_user_registration=message.chat.id
                return
        else:
            if message.text=="/start":
                if id_user_registration==0 or mode==2:
                    id_user_registration=message.chat.id
                    mode=1
                    await message.reply("Добро пожаловать! Подключить прокси? /yes или /no")
                else:
                    await message.reply("Кто-то уже регистрируется! Пожалуйста подождите!")
                return

def main():
    global bot
    def_sett()
    open_from_file()
    bot.add_handler(MessageHandler(bot_handl))
    bot.start()
    print('ID бота:', bot.get_me().id)
    for i in range(len(accounts_list)):
        try:
            accounts_list[i].client.start()
            accounts_list[i].client.send_message('me','Worked!')
            print('Аккаунт', i, 'запущен')
        except Exception as e:
            print(e)
            print('Ошибка')
    idle()
    for i in range(len(accounts_list)):
        try:
            accounts_list[i].client.stop()
            print('Аккаунт', i, 'запущен')
        except Exception:
            print('Ошибка')


if __name__ == '__main__':
    main()