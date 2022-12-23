timeout_rest = 24*60*60

from pathlib import Path
import sys
from pyrogram import Client, idle
from pyrogram.handlers import MessageHandler
from pyrogram.errors import RPCError, SessionPasswordNeeded, UserDeactivated, UserDeactivatedBan, AuthKeyDuplicated, UsernameNotOccupied, UserNotParticipant, ChatWriteForbidden, SlowmodeWait, ChannelPrivate, ChannelInvalid, ChatAdminRequired
from pyrogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import asyncio
from account import Account
import time
import os
from threading import Thread

def rest():
    global timeout_rest
    # print('.')
    for i in range(timeout_rest):
        time.sleep(1)
    print('restart')
    os.execv(sys.executable, ['python'] + sys.argv)

async def def_sett():
    global time_n, spam_tr, id_user_registration, accounts_list, help_str, username_acc, select_account, set_time, set_spam_text, set_spam_chats
    id_user_registration=0
    accounts_list=[]
    username_acc=[]
    set_time=[]
    set_spam_text=[]
    select_account = [[],[]]
    set_spam_chats=[]
    # time_n = int(datetime.now().timestamp())
    time_n = 0
    # count_sec = 0
    print(time_n)
    spam_tr = True
    help_str = '''
Доступны следущие команды:\n
/status – статус аккаунта\n
/set_timeout – установить таймаут\n
/set_spam_chats – ввести список каналов для спама\n
/set_spam_message – ввести список сообщений для спама\n
/apply_spam_message – применить список сообщений ко всем аккаунтам\n
/start_spam_all – начать спам на всех аккаунтах\n
/start_spam – начать спам\n
/stop_spam – остановить спам\n
/select_account – выбрать аккаунт для настройки\n
/start – добавить аккаунт\n
/help – список команд
'''

async def button_list(n_acc, id_user):
    if id_user in select_account[0]:
        if select_account[1][select_account[0].index(id_user)]!=-1:
            t = [KeyboardButton('/status'), KeyboardButton('/help')]
            if accounts_list[n_acc].spam:
                t.append(KeyboardButton('/stop_spam'))
            else:
                t.append(KeyboardButton('/start_spam'))
            return ReplyKeyboardMarkup([t], resize_keyboard=True)
    return ReplyKeyboardMarkup([[KeyboardButton('/select_account')]], resize_keyboard=True)
    # t = [KeyboardButton('/select_account')]

async def check_session_name(name):
    for acc in accounts_list:
        if name == acc.client.session_name:
            return False
    return True

async def new_session_name():
    i=0
    while True:
        name = 'account' + str(len(accounts_list) + i)
        if await check_session_name(name):
            return name
        else:
            i += 1

async def open_from_file():
    global bot, accounts_list
    with open('./bot_tokken.ini', 'r', encoding='utf-8') as fp:
        tok = fp.read().strip()
        bot = Client('bot', bot_token=tok)

    with open('./accounts.ini', 'r', encoding='utf-8') as fp:
        data = fp.readlines()
        for i in range(len(data)//2):
            accounts_list.append(Account(Client(data[2*i])))
            if data[2*i+1][0:4] == "None":
                pass
            else:
                prx=data[2*i+1].split()
                if prx[2] == 'n':
                    accounts_list[-1].client.proxy = dict(
                            hostname=prx[0],
                            port=int(prx[1]),
                            username=None,
                            password=None
                        )
                else:
                    accounts_list[-1].client.proxy = dict(
                            hostname=prx[0],
                            port=int(prx[1]),
                            username=prx[2],
                            password=prx[3]
                        )
    print('В работе ' + str(len(accounts_list)) + ' аккаунтов')
    try:
        fp = open('./account_timeout.ini', 'r', encoding='utf-8')
        lines = fp.readlines()
        for i in range(len(lines)//2):
            # print(lines[2*i])
            accounts_list[i].timeout = int(lines[2*i][:-1])
            # print(lines[2*i+1][:-1])
            if lines[2*i+1][:-1] in ['None', 'False', 'True']:
                accounts_list[i].spam = False
            else:
                accounts_list[i].message_id = int(lines[2*i+1][:-1])
                accounts_list[i].spam = True
                print(f'Спам в аккаунте {i} запущен')
    except Exception as e:
        print(e)
    with open('./message.ini', 'r', encoding='utf-8') as fp:
        data = fp.readlines()  
        for i in range(len(data)):
            accounts_list[i].message_list = data[i][:-1].split('&')
            # print(accounts_list[i].message_list)
        fp.close
    
async def open_chats():
    for i in range(len(accounts_list)):
        try:
            with(open(f'./chats/{username_acc[i]}.txt', 'r', encoding='utf-8')) as fp:
                data = fp.readlines()
                accounts_list[i].chats_list = data
                print(f'В аккаунте {username_acc[i]} {len(data)} чатов')
        except Exception:
                print(f'Чатов аккаунта {username_acc[i]} не найдено')

async def Save(t):
    if t == "Client":
        print('Save Client')
        with open('./accounts.ini', 'w', encoding='utf-8') as fp:
            fp.truncate(0)
            for acc in accounts_list:
                fp.write(await acc.client.export_session_string() + '\n')
                if acc.client.proxy == {}:
                    fp.write('None\n')
                elif acc.client.proxy.get('username') == None:
                    fp.write(acc.client.proxy.get('hostname') + " " + str(acc.client.proxy.get('port')) + ' n n\n')
                else:
                    fp.write(acc.client.proxy.get('hostname') + " " + str(acc.client.proxy.get('port')) + " " + acc.client.proxy.get('username') + " " + acc.client.proxy.get('password') + "\n")
            fp.close
    
    if t == "Message":
        print("Save message")
        with open('./message.ini', 'w', encoding='utf-8') as fp:
            fp.truncate(0)
            for acc in accounts_list:
                answ=""
                for mes in acc.message_list:
                    answ += mes +'&'
                if answ != "":
                    answ=answ[:-1] + '\n'
                else:
                    answ = "\n"
                fp.write(answ)
            fp.close

    if t == "Timeout":
        print("Save timeout")
        with open('./account_timeout.ini', 'w', encoding='utf-8') as fp:
            fp.truncate(0)
            for acc in accounts_list:
                fp.write(str(acc.timeout) + '\n')
                if acc.spam:
                    fp.write(f'{acc.message_id}\n')
                else:
                    fp.write('None\n')
            fp.close
                    
async def delete(dell, del_username = True):
    for i in range(len(dell)):
        n = dell[i] - i
        accounts_list.pop(n)
        if del_username:
            username_acc.pop(n)
        for k in select_account[1]:
            if k == n:
                k = -1
                id_d = select_account[0][select_account[1].index(k)]
                if id_d in set_time:
                    set_time.remove(id_d)
                if id_d in set_spam_text:
                    set_spam_text.remove(id_d)
                if id_d in set_spam_text:
                    set_spam_chats.remove(id_d)
    print(f'Удалены аккаунты {dell}')
    return True
    
async def spamming():
    global time_n, count_sec, spam_tr
    test_mode = False
    while spam_tr:
        for acc in accounts_list:
            if acc.spam:
                try:
                    n = accounts_list.index(acc)
                    user = username_acc[n]
                    t = time_n - acc.last_message
                    # print(f'Account {n}\nTime {t}\nMode {acc.mode}')
                    if 3 * t < acc.timeout and acc.mode == 'None':
                        acc.mode = 'Join'    
                        acc.w_chat = acc.spam_chat()
                        print(f'Работа с чатом: {acc.w_chat}')
                        if test_mode:
                            print(f'Вступил в {acc.w_chat}')
                        else:
                            acc.id_chat = (await acc.client.join_chat(acc.w_chat)).id
                    
                    if 3 * t > 2 * acc.timeout and t < acc.timeout and acc.mode == 'Join':
                        acc.mode = 'Leave'
                        if acc.p_chat != "":
                            try:
                                if test_mode:
                                    print(f'Покинул чат: {acc.p_chat}')
                                else:
                                    await acc.client.leave_chat(acc.p_chat)
                                
                            except UserNotParticipant:
                                pass
                            except UsernameNotOccupied:
                                pass
                            except Exception as e:
                                print(e)
                        acc.p_chat = acc.w_chat
                        
                    if t > acc.timeout:
                        acc.last_message = time_n
                        if acc.mode == 'Error':
                            acc.mode = 'None'
                        if acc.mode == 'Leave':
                            acc.mode = 'None'
                            if test_mode:
                                text = acc.spam_message()
                                print(f'Сообщение в {acc.id_chat} c текстом {text}')
                            else:
                                await acc.client.send_message(chat_id = acc.id_chat, text = acc.spam_message())
                            acc.count_success += 1
                            text = f'Сообщение отправленно\nЧат: @{acc.w_chat}\nАккаунт: @{user}\nЗа текущий сеанс отправленно {acc.count_success} сообщение (-й)'
                            print(acc.message_id)
                            await bot.send_message(chat_id = acc.message_id, text = text, disable_notification = True)
                    
                except UserDeactivatedBan:
                    await delete([accounts_list.index(acc)])
                    print(f'Аккаунт @{user} в бане')
                    await acc.client.send_message(chat_id = acc.message_id, text = f'Аккаунт {user} был деактивирован!')
                    return
                except UserDeactivated:
                    await delete([accounts_list.index(acc)])
                    print(f'Аккаунт @{user} в бане')
                    await acc.client.send_message(chat_id = acc.message_id, text = f'Аккаунт {user} был деактивирован!')
                    return
                except ChannelPrivate:
                    print(f'Чат @{acc.w_chat} приватный')
                    acc.mode = 'Error'
                except ChannelInvalid:
                    print(f'Чат @{acc.w_chat} не найден')
                    acc.mode = 'Error'
                except UsernameNotOccupied:
                    print(f'Чат @{acc.w_chat} не найден')
                    acc.mode = 'Error'
                except UserNotParticipant:
                    pass
                except ChatWriteForbidden:
                    print(f'Сообщения в чате @{acc.w_chat} запрещены')
                    acc.mode = 'Error'
                except SlowmodeWait:
                    print(f'В чате @{acc.w_chat} «медленный режим» отправки сообщений')
                    acc.mode = 'Error'
                except ChatAdminRequired:
                    print(f'Для отправки сообщения в чат @{acc.w_chat} требуются права администратора')
                    acc.mode = 'Error'
                except Exception as e:
                    print(e)
                    acc.mode = 'Error'
        await asyncio.sleep(5)
        time_n += 5
        if time_n > 100000:
            print('Upd time')
            time_n = 0
            for acc in accounts_list:
                acc.last_message = 0

async def success_login(message):
    global id_acc, answer_list, id_user,level_users,stt_reg,mode, id_user_registration, help_str, username_acc, select_account
    print("Успешный вход!")
    id_user_registration=0
    mode=0
    if len(accounts_list) > 1:
        accounts_list[-1].message_list = accounts_list[0].message_list
        await message.reply('Вход выполнен успешно!\n' + help_str)
    else:
        set_spam_text.append(message.chat.id)
        await message.reply('Вводите сообщения для спама\n/clear – очистить список сообщений\n/save – сохранить список сообщений', reply_markup=ReplyKeyboardMarkup([[KeyboardButton('/clear'), KeyboardButton('/save')]]))
    await accounts_list[-1].client.disconnect()
    await accounts_list[-1].client.start()
    await Save("Client")
    await Save("Message")
    await Save("Timeout")
    username_acc.append((await accounts_list[-1].client.get_me()).username)
    if message.chat.id in select_account[0]:
        select_account[1][select_account[0].index(message.chat.id)] = len(accounts_list) - 1

    else:
        select_account[0].append(message.chat.id)
        select_account[1].append(len(accounts_list)-1)
    
async def start_spam(n, message):
    accounts_list[n].spam = True
    accounts_list[n].message_id = message.chat.id
    await Save("Timeout")

async def bot_handl(client, message):
    global proxyb, proxyc, mode, id_user_registration, code, set_spam_chats, phonehash, accounts_list, phonenumber, code, select_account, set_time, set_spam_text
    # print(message.text)
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
                    accounts_list.append(Account(Client(await new_session_name(), proxy=None)))
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
                        accounts_list.append(Account(Client(await new_session_name(), proxy=proxyc)))
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
                            accounts_list.append(Account((Client(await new_session_name(), proxy=proxyc))))
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
                await message.reply("Добро пожаловать! Подключить прокси? /yes или /no", reply_markup = ReplyKeyboardRemove())
                id_user_registration=message.chat.id
                return
        else:
            if message.text=="/start":
                if id_user_registration==0 or mode==2:
                    id_user_registration=message.chat.id
                    mode=1
                    await message.reply("Добро пожаловать! Подключить прокси? /yes или /no", reply_markup = ReplyKeyboardRemove())
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
                await message.reply(answ, reply_markup = ReplyKeyboardRemove())
            
            if message.text == '/bot_stop':
                        exit()

            if message.text == '/start_spam_all':
                for n in range(len(accounts_list)):
                    await start_spam(n, message)
                    print(f'Запущен спам на {n} аккаунте')
                await message.reply(f'Запущен спам на {n+1} аккаунтах', reply_markup=await button_list(n, message.chat.id))
                return

            if message.chat.id in select_account[0]:
                n = select_account[1][select_account[0].index(message.chat.id)]
                
                if not message.text is None:
                    if message.text[:5] == '/bot_':
                        select_account[1][select_account[0].index(message.chat.id)] = username_acc.index(message.text[5:])
                        await message.reply('Выбран аккаунт: ' + message.text[5:], reply_markup=await button_list(select_account[1][select_account[0].index(message.chat.id)], message.chat.id))
                        print(select_account)
                        return
                
                if n!=-1:
                    if message.text == '/clear':
                        accounts_list[n].message_list=[]
                        await message.reply('Список спам сообщений очищен!')    
                        return
                    
                    if message.text == '/save':
                        set_spam_text.remove(message.chat.id)
                        await Save("Message")
                        await message.reply('Сохраненно\n/apply_spam_message – применить список сообщений ко всем ботам\n/start_spam – начать спам', reply_markup=await button_list(n, message.chat.id))
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
                        await Save("Timeout")
                        set_time.remove(message.chat.id)
                        return
                    
                    if message.text == '/set_timeout':
                        set_time.append(message.chat.id)
                        await message.reply('Введите таймаут (сек)')
                        return
                    
                    if message.text == '/set_spam_message':
                        set_spam_text.append(message.chat.id)
                        await message.reply('Вводите сообщения для спама\n/clear – очистить список сообщений\n/save – сохранить список сообщений', reply_markup=ReplyKeyboardMarkup([[KeyboardButton('/clear'), KeyboardButton('/save')]], resize_keyboard=True))
                        return
                    
                    
                        
                    if message.text == '/set_spam_chats':
                        set_spam_chats.append(message.chat.id)
                        await message.reply('Прикрепите к сообщению файл txt, cо списком **ссылок** на чаты\nПример:\nhttps://t.me/liberoofficialgroup\nhttps://t.me/fegchat\nhttps://t.me/virtchat35', disable_web_page_preview = True)
                        return
                    


                    if message.text == '/start_spam':
                        if not accounts_list[n].spam:
                            await start_spam(n, message)
                            await message.reply('Спам запущен\n/status – посмотреть статус', reply_markup=await button_list(n, message.chat.id))             
                        else:
                            await message.reply('Спам уже запущен\n/status – посмотреть статус')
                            
                    if message.text == '/stop_spam':
                        if accounts_list[n].spam:
                            accounts_list[n].spam = False
                            accounts_list[n].p_chat = ''
                            await Save("Timeout")
                            await message.reply(f'Спам остановлен\nОтправленно {accounts_list[n].count_success} сообщений', reply_markup=await button_list(n, message.chat.id))
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
                        return

                    if message.text == '/apply_spam_message':
                        for app in accounts_list:
                            app.message_list = accounts_list[n].message_list
                        await Save("Message")
                        await message.reply('Список сообщения продублирован на все аккаунты')
                        return

                else:
                    if message.text != '/select_account':
                        await message.reply('Выберите аккаунт с помощью команды /select_account', reply_markup=await button_list(0, message.chat.id))
            else:
                select_account[0].append(message.chat.id)
                select_account[1].append(-1)
                if message.text != '/select_account':
                    await message.reply('Выберите аккаунт с помощью команды /select_account', reply_markup=await button_list(0, message.chat.id))
                print(select_account)

async def main():
    global bot, username_acc
    print('Spambot v3.3.2')
    await def_sett()
    await open_from_file()
    bot.add_handler(MessageHandler(bot_handl))
    try:
        await bot.start()
        print('Username бота:', (await bot.get_me()).username)
    except UserDeactivated:
        print('Бот был забанен! Замените токкен!')
    except UserDeactivatedBan:
        print('Бот был забанен! Замените токкен!')
    except Exception as e:
        print(e)
    dell = []    
    for i in range(len(accounts_list)):
        try:
            await accounts_list[i].client.start()
            user = (await accounts_list[i].client.get_me()).username
            username_acc.append(user)
            print(f'Аккаунт {user} запущен')
        except UserDeactivated:
            dell.append(i)
            print(f'Аккаунт {i} забанен')
        except UserDeactivatedBan:
            dell.append(i)
            print(f'Аккаунт {i} забанен')
        except AuthKeyDuplicated:
            dell.append(i)
        except IndexError:
            break
        except Exception:
            pass
    await delete(dell, False)
    # print(username_acc)
    # print(len(accounts_list))
    await Save("Client")
    await Save("Message")
    await Save("Timeout")
    print(username_acc)
    await open_chats()
    Thread(target = rest).start()
    await spamming()
    await idle()
    for i in range(len(accounts_list)):
        try:
            await accounts_list[i].client.stop()
        except Exception:
            print('Ошибка')

if __name__ == '__main__':
    # try:
    asyncio.run(main())
    # except Exception as e:
    #     print(e)
    time.sleep(15)
