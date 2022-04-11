import os
from pathlib import Path
import sys
from pyrogram import Client, Clienttt, idle
from pyrogram.handlers import MessageHandler
from pyrogram.errors import RPCError, SessionPasswordNeeded, UserDeactivated, UserDeactivatedBan
from pyrogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import asyncio
from account import Account

def def_sett():
    global id_user_registration, accounts_list, mode_temp, mode_acc, help_str, username_acc, select_account, set_time, set_spam_text, set_spam_chats
    id_user_registration=0
    accounts_list=[]
    mode_temp=None
    mode_acc=[]
    username_acc=[]
    set_time=[]
    set_spam_text=[]
    select_account = [[],[]]
    set_spam_chats=[]
    help_str = '''
Доступны следущие команды:\n
/status – статус аккаунта\n
/set_timeout – установить таймаут\n
/set_spam_chats – ввести список каналов для спама\n
/set_spam_message – ввести список сообщений для спама\n
/start_spam – начать спам\n
/stop_spam – остановить спам\n
/select_account – выбрать аккаунт для настройки\n
/start – добавить аккаунт\n
/help – список команд
'''

def resource_path(relative):
    return Path(sys.argv[0]).parent/relative

def open_from_file():
    global bot, accounts_list
    with open(resource_path('bot_tokken.ini'), 'r', encoding='utf-8') as fp:
        bot = Clienttt('bot', bot_token=fp.read())
    with open(resource_path('accounts.ini'), 'r', encoding='utf-8') as fp:
        data = fp.read()
        for line in data.splitlines():
            accounts_list.append(Account(Client(line)))
        print('В работе ' + str(len(accounts_list)) + ' аккаунтов')
        

def open_chats():
    for i in range(len(accounts_list)):
        try:
            with(open(Path(sys.argv[0]).parent/f'chats/{username_acc[i]}.txt', 'r', encoding='utf-8')) as fp:
                data = fp.readlines()
                accounts_list[i].chats_list = data
                print('Всего чатов', len(data))
        except Exception:
                print(f'Чатов аккаунта {i} не найдено')

async def Save(t):
    if t == "Client":
        print('Save Client')
        with open(resource_path('accounts.ini'), 'w', encoding='utf-8') as fp:
            for acc in accounts_list:
                fp.write(await acc.client.export_session_string())
            fp.close

def delete(n):
    accounts_list.pop(n)
    username_acc.pop(n)
    asyncio.run(Save("Client"))
    return True
    
async def spamming(n, message):
    await message.repy('Спам запущен')
    accounts_list[n].count_success = 0
    chat_prev = ""
    while accounts_list[n].spam:
        try:
            t=accounts_list[n].timeout
            
            chat = accounts_list[n].spam_chat()
            print(chat)
            chatid = (await accounts_list[n].client.join_chat(chat)).id
            await asyncio.sleep(accounts_list[n].timeout/3)
            t -= t/3
            
            if chat_prev != "":
                try:
                    await accounts_list[n].client.leave_chat(chat_prev)
                except Exception as e:
                    print(e)
            chat_prev = chat
            
            await asyncio.sleep(accounts_list[n].timeout/3)
            t -= t/3
            
            await accounts_list[n].client.send_message(chat_id = chatid, text = accounts_list[n].spam_message())
            accounts_list[n].count_success += 1
            await message.reply(f'Отпрваленно сообщение в @{chat}\nЗа текущий сеанс отправленно {accounts_list[n].count_success} сообщений')
            
            await asyncio.sleep(accounts_list[n].timeout/3)
            t -= t/3
            
            
        except UserDeactivatedBan:
            delete(n)
            print(f'Аккаунт {username_acc[n]} в бане')
            await message.reply(f'Аккаунт {username_acc[n]} был деактивирован!')
            return
        except Exception as e:
            print(e)
            # FLOOD_WAIT_X
            # SLOWMODE_WAIT_X
            # USERNAME_NOT_OCCUPIED
            # CHAT_WRITE_FORBIDDEN
            await asyncio.sleep(t)
    
async def success_login(message):
    global id_acc, answer_list, id_user,level_users,stt_reg,mode, id_user_registration, mode_acc, help_str, username_acc, select_account
    print("Успешный вход!")
    id_user_registration=0
    mode_acc.append("Null")
    mode=0
    await accounts_list[-1].client.disconnect()
    await accounts_list[-1].client.start()
    await Save("Client")
    username_acc.append((await accounts_list[-1].client.get_me()).username)
    if message.chat.id in select_account[0]:
        select_account[1][select_account[0].index(message.chat.id)] = len(accounts_list) - 1
    else:
        select_account[0].append(message.chat.id)
        select_account[1].append(len(accounts_list)-1)
    await message.reply('Вход выполнен успешно!\n' + help_str)

async def bot_handl(client, message):
    global proxyb, proxyc, mode, id_user_registration, code, set_spam_chats, phonehash, accounts_list, phonenumber, code, select_account, set_time, set_spam_text
    print(message.text)
    # if not message.text is None:
    if True:
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
                    await message.reply("Произошла ошибка! Повторить попытку? /try\nЛибо ведите другие hostname и порт\n/without_proxy – подключиться без прокси")
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

            if message.text == '/help':
                await message.reply(help_str)
                return
            
            if message.text == '/select_account':
                answ='Выберите бот для настройки\n'
                for name in username_acc:
                    answ += '/bot_' + name + '\n'
                await message.reply(answ)
            
            if message.text == '/bot_stop':
                        exit()
                        
            if message.chat.id in select_account[0]:
                n = select_account[1][select_account[0].index(message.chat.id)]
                
                if not message.text is None:
                    if message.text[:5] == '/bot_':
                        select_account[1][select_account[0].index(message.chat.id)] = username_acc.index(message.text[5:])
                        await message.reply('Выбран аккаунт: ' + username_acc[n] , reply_markup=ReplyKeyboardMarkup([[KeyboardButton('/status'), KeyboardButton('/help'), KeyboardButton('/start_spam')]]))
                        print(select_account)
                        return
                
                if n!=-1:
                    if message.text == '/clear':
                        accounts_list[n].message_list=[]
                        await message.reply('Список спам сообщений очищен!')    
                        return
                    
                    if message.text == '/save':
                        set_spam_text.remove(message.chat.id)
                        await message.reply('Сохраненно\n/start_spam – начать спам', reply_markup=ReplyKeyboardMarkup([[KeyboardButton('/status'), KeyboardButton('/start_spam')]]))
                        return
                    
                    if message.chat.id in set_spam_text:
                        accounts_list[n].message_list.append(message.text)
                        print(accounts_list[n].message_list)
                        return
                    
                    if message.chat.id in set_spam_chats:
                        
                        try:
                            path=await bot.download_media(message=message, file_name = f'./chats/{username_acc[n]}.txt')
                            print(f'Файл сохранен: {path}')
                            with open(path, mode = 'r') as fp:
                                accounts_list[n].chats_list = fp.readlines()
                            await message.reply('Получилось извлечь ' + str(len(accounts_list[n].chats_list)) + ' чат(-ов)')
                        except Exception as e:
                            print(e)
                            await message.reply('Ошибка')
                        finally:
                            set_spam_chats.remove(message.chat.id)
                    
                    if message.chat.id in set_time:
                        accounts_list[n].timeout=int(message.text)
                        await message.reply('Таймаут ' + str(accounts_list[n].timeout) + ' секунд')
                        set_time.remove(message.chat.id)
                        return
                    
                    if message.text == '/set_timeout':
                        set_time.append(message.chat.id)
                        await message.reply('Введите таймаут (сек)')
                        return
                    
                    if message.text == '/set_spam_message':
                        set_spam_text.append(message.chat.id)
                        await message.reply('Вводите сообщения для спама\n/clear – очистить список сообщений\n/save – сохранить список сообщений', reply_markup=ReplyKeyboardMarkup([[KeyboardButton('/clear'), KeyboardButton('/save')]]))
                        return
                    
                    
                        
                    if message.text == '/set_spam_chats':
                        set_spam_chats.append(message.chat.id)
                        await message.reply('Прикрепите к сообщению файл txt, cо списком **ссылок** на чаты\nПример:\nhttps://t.me/liberoofficialgroup\nhttps://t.me/fegchat\nhttps://t.me/virtchat35')
                        return
                    
                    if message.text == '/start_spam':
                        if not accounts_list[n].spam:
                            accounts_list[n].spam = True
                            await spamming(n, message)
                            await message.reply('Спам запущен\n/status – посмотреть статус', reply_markup=ReplyKeyboardMarkup([[KeyboardButton('/status'), KeyboardButton('/stop_spam')]]))
                        else:
                            await message.reply('Спам уже запущен\n/status – посмотреть статус')
                            
                    if message.text == '/stop_spam':
                        if accounts_list[n].spam:
                            accounts_list[n].spam = False
                            await message.reply(f'Спам остановлен\nОтправленно {accounts_list[n].count_success} сообщений', reply_markup=ReplyKeyboardMarkup([[KeyboardButton('/start_spam')]]))
                        else:
                            await message.reply('Спам не запущен')
                        return
                    
                    if message.text == '/status':
                        acc = await accounts_list[n].client.get_me()
                        # print(acc)
                        answ = f'Аккаунт **{acc.username}**\nТаймаут: **{accounts_list[n].timeout}** секунд\n'
                        if accounts_list[n].spam:
                            answ+=f'Спам **запущен**\nНа текущий момент отправленно **{accounts_list[n].count_success}** сообщений\n'
                        else:
                            answ+='Спам **остановлен**\n'
                        answ+='В спам листе **' + str(len(accounts_list[n].message_list)) + '** сообщений\nРассылка ведется в **' + str(len(accounts_list[n].chats_list)) + '** чат(-ов)\n'
                        if not (acc.is_scam and acc.is_fake):
                            answ+='Ограничений на аккаунте **нет**'
                        else:
                            answ+='На аккаунте **ограничения**\n'
                        await message.reply(answ)
                else:
                    if message.text != '/select_account':
                        await message.reply('Выберите аккаунт с помощью команды /select_account', reply_markup=ReplyKeyboardMarkup([[KeyboardButton('/select_account')]]))
            else:
                select_account[0].append(message.chat.id)
                select_account[1].append(-1)
                if message.text != '/select_account':
                    await message.reply('Выберите аккаунт с помощью команды /select_account', reply_markup=ReplyKeyboardMarkup([[KeyboardButton('/select_account')]]))
                print(select_account)

                    

def main():
    global bot, username_acc
    print(str(Path(sys.argv[0]).parent/'chats'))
    def_sett()
    open_from_file()
    bot.add_handler(MessageHandler(bot_handl))
    
    try:
        bot.start()
        print('ID бота:', bot.get_me().id)
    except UserDeactivated:
        print('Бот был забанен! Замените токкен!')
    except UserDeactivatedBan:
        print('Бот был забанен! Замените токкен!')
        
    for i in range(len(accounts_list)):
        try:
            accounts_list[i].client.start()
            username_acc.append(accounts_list[i].client.get_me().username)
            print('Аккаунт', i, 'запущен')
        except UserDeactivated:
            if delete(i):
                print('Удален бот ' + str(i))
                i-=1
        except UserDeactivatedBan:
            if delete(i):
                print('Удален бот ' + str(i))
                i-=1
        except Exception as e:
            print(e)
            print('Ошибка')
            
    print(username_acc)
    open_chats()
    idle()
    for i in range(len(accounts_list)):
        try:
            accounts_list[i].client.stop()
        except Exception:
            print('Ошибка')


if __name__ == '__main__':
    main()