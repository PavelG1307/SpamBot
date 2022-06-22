from configparser import NoOptionError
import os
from pathlib import Path
import sys
import time
from pyrogram import Client, idle, filters
from pyrogram.handlers import MessageHandler
from pyrogram.errors import RPCError, SessionPasswordNeeded
import asyncio

id = [18428876,19543614,9696471]
hash = ["ef370365768e81f55c42f96ea4858bc5","ccfbfe4f133fff8279e8031797adfdd7","6181f0cc6d734e181c2aec501d691eb9"]
select_id=1

def resource_path(relative):
    return Path(sys.argv[0]).parent/relative

def select_id_plus():
    global select_id, id
    select_id+=1
    if select_id>=len(id):
        select_id=0

def bot_setup():
    global mybot
    f=open(resource_path('bot_settings.ini'),'r', encoding='utf-8')     
    token = f.readline()[7:]
    sessionname=token[:10]
    f.close() 
    mybot = Client(
        sessionname,
        bot_token=token,
        api_id=id[0],
        api_hash=hash[0]
    )
    
def def_sett():
    global id_bot, id_acc, layout, stt_reg, accounts, answer_list, id_user, level_users, n, mode, id_user_registration, input_tokken, settings_templates, id_creator_templates, mode_temp, proxyc, mode_rule, id_of_interlocutor
    id_bot = 0
    id_acc = []
    layout = []
    stt_reg = ""
    accounts = []
    answer_list = []
    id_user = []
    level_users = []
    n = 0
    mode=0
    id_user_registration=0
    input_tokken=False
    settings_templates=[]
    id_creator_templates=0
    mode_temp="None"
    mode_rule=[]
    proxyc = dict(hostname=None, port=None, username=None, password=None)
    id_of_interlocutor=[]

def openfromfile():
    global accounts, proxyc, select_id, settings_templates, mode_rule
    try:
        f = open(resource_path('accounts.ini'), 'r', encoding='utf-8')
        lines = f.readline().split(" ")
        for i in range(len(lines)//6):
            if lines[6*i+2]=="n" and lines[6*i+3]=="n" and lines[6*i+4]=="n" and lines[6*i+5]=="n":
                accounts.append(Client(str(lines[6*i]), api_id=id[select_id], api_hash=hash[select_id], proxy=None))
            if lines[6*i+2]!="n" and lines[6*i+3]!="n" and lines[6*i+4]=="n" and lines[6*i+5]=="n":
                accounts.append(Client(str(lines[6*i]), api_id=id[select_id], api_hash=hash[select_id],proxy = dict(hostname=lines[6*i+2], port=int(lines[6*i+3]))))
            if lines[6*i+2]!="n" and lines[6*i+3]!="n" and lines[6*i+4]!="n" and lines[6*i+5]!="n":
                accounts.append(Client(str(lines[6*i]), api_id=id[select_id], api_hash=hash[select_id],proxy = dict(hostname=lines[6*i+2], port=int(lines[6*i+3]), username=lines[6*i+4], password=lines[6*i+5])))
            print("account:", accounts[i].session_name)
            print("proxy:", accounts[i].proxy)
            id_user.append([])
            level_users.append([])
            id_acc.append(int(lines[6*i+1]))
            accounts[-1].add_handler(MessageHandler(answer, filters.private))
            select_id_plus()
            
        f.close()
        print("Account ids:",id_acc)
    except Exception as e:
        print(e)
    try:
        f = open(resource_path('answer.ini'), 'r', encoding='utf-8')
        lines = f.readlines()
        for line in lines:
            if line[:1] == "b":
                answer_list.append([])
            if len(line)<=3 and line[:1] == "l":
                    answer_list[-1].append([[""]])
            else:
                if line[:2] == "l:":    
                    words = line[2:-1].split('_')
                    answer_list[-1].append([[""]])
                    for word in words:
                        answer_list[-1][-1][0].append(word)
            if line[:1] == "o":
                words = line[2:-1].split()
                answer_list[-1][-1].append([[]])
                for word in words:
                    answer_list[-1][-1][1][0].append(int(word))
                
            if line[:2] == "tb":
                answer_list[-1][-1].append([[]])
                words = line[3:-1].split()
                for word in words: answer_list[-1][-1][2][0].append(int(word))
                
            if line[:2] == "ta":
                if len(line)>4:
                    fline=line[3:-1].split(';')
                    for fl in fline:
                        answer_list[-1][-1][2].append([])
                        words=fl.split()
                        for word in words: answer_list[-1][-1][2][-1].append(int(word))
                
                
            if line[:1] == "k":
                if len(line)>4:
                    fline=line[2:-1].split(';')
                    for fl in fline:
                        answer_list[-1][-1][1].append([])
                        words=fl.split()
                        for word in words: answer_list[-1][-1][1][-1].append(int(word))
        for i in range(len(answer_list)):
            layout.append(len(answer_list[i])-1)
            if layout[i]>=0:
                mode_rule.append("Keyword")
            else:
                mode_rule.append("Basic")
                layout[i]=0
        f.close()
        print("Rule number:",layout)
        print("Rules:",answer_list)
    except Exception as e:
        print(e)
    try:
        f = open(resource_path('templates.ini'), 'r', encoding='utf-8')
        lines = f.readlines()
        for line in lines:
            if line[:2]=="nm":
                settings_templates.append([line[3:-1]])
            if line[:2]=="id":
                settings_templates[-1].append(int(line[3:-1]))
            if line[:2]=="lt":
                settings_templates[-1].append([[],[[]],[[]]])
                if len(line)>4:
                    words=line[3:-1].split('_')
                    for word in words:
                        settings_templates[-1][-1][0].append(word)
            if line[:2]=="bm":
                if len(line)>4:
                    words=line[3:-1].split()
                    for word in words:
                        settings_templates[-1][-1][1][0].append(int(word))
            if line[:2]=="aw":
                if len(line)>4:
                    fline=line[3:-1].split(';')
                    print(fline)
                    for ln in fline:
                            settings_templates[-1][-1][1].append([])
                            words=ln.split()
                            for word in words:
                                settings_templates[-1][-1][1][-1].append(int(word))
            if line[:2]=="tb":
                if len(line)>4:
                    words=line[3:-1].split()
                    for word in words:
                        settings_templates[-1][-1][2][0].append(int(word))
            if line[:2]=="ta":
                if len(line)>4:
                    fline=line[3:-1].split(';')
                    print(fline)
                    for ln in fline:
                            settings_templates[-1][-1][2].append([])
                            words=ln.split()
                            for word in words:
                                settings_templates[-1][-1][2][-1].append(int(word))
        f.close()
        print("Templates:", settings_templates)
    except Exception as e:
        print(e)
    try:
        f = open(resource_path('users.ini'), 'r', encoding='utf-8')
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i][:-1]!="n":
                words = lines[i][:-1].split()
                for k in range(len(words)//2):
                    id_user[i].append(int(words[2*k]))
                    level_users[i].append(int(words[2*k+1]))
        f.close()
        print(id_user)
    except Exception as e:
        print(e)

def ClearAll():
    f = open(resource_path('accounts.ini'), 'w')
    f.truncate(0)
    f = open(resource_path('users.ini'), 'w')
    f.truncate(0)
    f = open(resource_path('answer.ini'), 'w')
    f.truncate(0)
    f.close()
    def_sett()

def SaveClient():
    f = open(resource_path('accounts.ini'), 'w', encoding='utf-8')
    f.truncate(0)
    savestr = ""
    for i in range(len(accounts)):
        print(accounts[i].proxy)
        if accounts[i].proxy == {}:
            savestr += accounts[i].session_name + " " + str(id_acc[i])+" n n n n "
        else:
            try:
                if accounts[i].proxy.get('username') == None:
                    savestr += accounts[i].session_name + " " + str(id_acc[i])+" " + accounts[i].proxy.get('hostname') + " " + str(accounts[i].proxy.get('port')) + " n n "
                else:
                    savestr += accounts[i].session_name + " " + str(id_acc[i]) + " " + accounts[i].proxy.get('hostname') + " " + str(accounts[i].proxy.get(
                        'port')) + " " + accounts[i].proxy.get('username') + " " + accounts[i].proxy.get('password') + " "
            except Exception:
                    savestr += accounts[i].session_name + " " + str(id_acc[i]) + " " + accounts[i].proxy.get('hostname') + " " + str(accounts[i].proxy.get(
                        'port')) + " " + accounts[i].proxy.get('username') + " " + accounts[i].proxy.get('password') + " "
    print(savestr)
    f.write(savestr)
    print(savestr)
    print("Save Client")
    f.close()

def SaveAnswer():
    f = open(resource_path('answer.ini'), 'w', encoding='utf-8')
    f.truncate(0)
    for i in range(len(answer_list)):
        f.write("b:"+"\n")
        for j in range(len(answer_list[i])):
            answ = "l:"
            if len(answer_list[i][j][0]) < 2:
                f.write("l:"+"\n")
            else:
                for k in range(1, len(answer_list[i][j][0])):
                    answ += str(answer_list[i][j][0][k])+"_"
                f.write(answ[:-1]+"\n")
            answ = "o:"
            for k in range(len(answer_list[i][j][1][0])):
                answ += str(answer_list[i][j][1][0][k])+" "
            f.write(answ[:-1]+"\n")
            answ = "k:"
            for k in range(1, len(answer_list[i][j][1])):
                for l in answer_list[i][j][1][k]:
                    answ += str(l)+" "
                answ=answ[:-1]
                answ+=';'
            f.write(answ[:-1]+"\n")
            answ = "tb:"
            for k in range(len(answer_list[i][j][2][0])):
                answ += str(answer_list[i][j][2][0][k])+" "
            f.write(answ[:-1]+"\n")
            answ = "ta:"
            for k in range(1, len(answer_list[i][j][2])):
                for l in answer_list[i][j][2][k]:
                    answ += str(l)+" "
                answ=answ[:-1]
                answ+=';'
            f.write(answ[:-1]+"\n")
    f.close()

def SaveUsers():
    f = open(resource_path('users.ini'), 'w', encoding='utf-8')
    print("Users:",str(id_user))
    f.truncate(0)
    for i in range(len(id_user)):
        answ = ""
        for j in range(len(id_user[i])):
            answ += str(id_user[i][j])+" " + str(level_users[i][j])+" "
        if answ!="":
            answ = answ[:-1]+"\n"
        else:
            answ = "n\n"
        f.write(answ)
    f.close()

def SaveTemplate():
    global settings_templates
    f = open(resource_path('templates.ini'), 'w', encoding='utf-8')
    print("Templates:",str(settings_templates))
    f.truncate(0)
    for i in range(len(settings_templates)):
        f.write("nm:" + settings_templates[i][0]+'\n')
        f.write("id:" + str(settings_templates[i][1])+'\n')
        for j in range(2,len(settings_templates[i])):
            answ="lt:"
            for k in range(len(settings_templates[i][j][0])):
                answ+=settings_templates[i][j][0][k]+"_"
            if len(answ)>3:
                answ=answ[:-1]
            f.write(answ+'\n')
            answ="bm:"
            for k in range(len(settings_templates[i][j][1][0])):
                answ+=str(settings_templates[i][j][1][0][k])+" "
            if len(answ)>3:
                answ=answ[:-1]
            f.write(answ+'\n')
            answ="aw:"
            for k in range(1,len(settings_templates[i][j][1])):
                for l in settings_templates[i][j][1][k]:
                    answ+=str(l)+" "
                answ=answ[:-1]
                answ+=";"
            if len(answ)>3:
                answ=answ[:-1]
            f.write(answ+'\n')
            answ="tb:"
            for k in range(len(settings_templates[i][j][2][0])):
                answ+=str(settings_templates[i][j][2][0][k])+" "
            if len(answ)>3:
                answ=answ[:-1]
            f.write(answ+'\n')
            answ="ta:"
            for k in range(1,len(settings_templates[i][j][2])):
                for l in settings_templates[i][j][2][k]:
                    answ+=str(l)+" "
                answ=answ[:-1]
                answ+=";"
            if len(answ)>3:
                answ=answ[:-1]
            f.write(answ+'\n')
            print("Successfully saved!")
    f.close()

async def help_message(message):
    await message.reply(
"Механизм ответа бота основан на правилах. Каждое правило состоит из:\n\
\n\
1. Основная фраза – фраза которая появляется в случае необнаружения сходств с ключевыми словами,\n\
2. Ключевые слова – слова которые будут искаться в сообщениях\n\
3. Ответы на сообщения\n\
\n\
Команды:\n\
\n\
/create_template – создать шаблон\n\
/apply – применить к данному боту шаблон\n\
/delete_template – удалить шаблон\n\
\n\
/new_rules – сбросить правила у данного бота\n\
/clear_user_history – сбросить прогресс пользователей\n\
\n\
/help – посмотреть подсказку\n\
/set_tokken – сменить бота\n\
\n\
/hard_reset – сброс всех аккаунтов\n\
\n\
P.s. не очищайте данный чат"
    )

async def success_login(n, message):
    global accounts, id_acc, answer_list, id_user,level_users,stt_reg,mode, id_user_registration, mode_rule
    print("Успешный вход!")
    id_user_registration=0
    accounts[n].add_handler(MessageHandler(answer, filters.private))
    await accounts[n].disconnect()
    answer_list.append([])
    id_user.append([])
    level_users.append([])
    mode_rule.append("Basic")
    select_id_plus()
    mode=0
    print("Connect")
    await accounts[n].start()
    m=(await accounts[n].get_me()).id
    if m!=message.chat.id:
        message.reply("Дальнейщие настройки бота возможны только с рабочего аккаунта!")
    id_acc.append(m)
    SaveClient()
    SaveAnswer()
    SaveUsers()
    await message.reply("Вход выполнен успешно!\nПожалуста подождите 10 секунд и выберите нужную команду:\n/apply – применить шаблон\n/create_template – создать шаблон\n/create_rule – создать свои правила\n/help – посмотреть подсказку")
    os.execv(sys.executable, ['python'] + sys.argv)

async def ApplyMessage(client,message,id,i,n):
    global settings_templates, mode_temp, answer_list, count, layout
    layout[n]=0
    answer_list[n]=[]
    for j in range(2,len(settings_templates[i])):
        answer_list[n].append([[''],[[]],[]])
        for word in settings_templates[i][j][0]:
            answer_list[n][-1][0].append(word)
        
        for k in range(len(settings_templates[i][j][2])):
            answer_list[n][-1][2].append([])
            for l in range(len(settings_templates[i][j][2][k])):
                answer_list[n][-1][2][k].append(settings_templates[i][j][2][k][l])
    for j in range(2,len(settings_templates[i])):
        mode_temp = "ApplyBasic"
        for k in range(len(settings_templates[i][j][1][0])):
            await client.forward_messages(chat_id=message.chat.id, from_chat_id=id_bot,message_ids=settings_templates[i][j][1][0][k], scrit=True)
            await asyncio.sleep(4)
        mode_temp = "ApplyMessage"
        for k in range(1,len(settings_templates[i][j][1])):
            answer_list[n][layout[n]][1].append([]) 
            for l in range(len(settings_templates[i][j][1][k])):
                await client.forward_messages(chat_id=message.chat.id, from_chat_id=id_bot,
                                                        message_ids=settings_templates[i][j][1][k][l], scrit=True)   
                await asyncio.sleep(4)
        await asyncio.sleep(1)
        layout[n]+=1
        SaveAnswer()
    print(answer_list[n])
    await message.reply('Бот настроен!')
    mode_temp = "None"

async def answer(client, message):
    global n, mode_rule, id_of_interlocutor
    if client in accounts:
        m = accounts.index(client)
        if message.chat.id != id_bot and message.from_user.id != id_acc[m]:
            if not (message.chat.id in id_user[m]):
                id_user[m].append(message.chat.id)
                level_users[m].append(0)
                SaveUsers()
            k = id_user[m].index(message.chat.id)
            if k != -1 and not (message.chat.id in id_of_interlocutor):
                id_of_interlocutor.append(message.chat.id)
                send_mess = True
                if level_users[m][k] < len(answer_list[m]):
                    if not (message.text is None):
                        for j in range(1, len(answer_list[m][level_users[m][k]][0])):
                            if message.text.lower().find(answer_list[m][level_users[m][k]][0][j]) != -1:
                                for h in range(len(answer_list[m][level_users[m][k]][1][j])):
                                    print('k',k)
                                    print('Timeout:', answer_list[m][level_users[m][k]][2][j][h],'s')
                                    await asyncio.sleep(answer_list[m][level_users[m][k]][2][j][h])
                                    print('message_ids',answer_list[m][level_users[m][k]][1][j][h])
                                    await client.forward_messages(chat_id=message.chat.id, from_chat_id=id_bot, message_ids=answer_list[m][level_users[m][k]][1][j][h], scrit=True)
                                    send_mess = False
                    if send_mess:
                        print(answer_list[m][level_users[m][k]][1][0])
                        for i in range(len(answer_list[m][level_users[m][k]][1][0])):
                            print('Timeout:', answer_list[m][level_users[m][k]][2][0][i],'s')
                            await asyncio.sleep(answer_list[m][level_users[m][k]][2][0][i])
                            await client.forward_messages(chat_id=message.chat.id, from_chat_id=id_bot, message_ids=answer_list[m][level_users[m][k]][1][0][i], scrit=True)
                        level_users[m][k] += 1
                        SaveUsers()
                id_of_interlocutor.remove(message.chat.id)
        else:
            print("Message userbot")
            print('Mode', mode_rule[m])
            if len(id_acc)>m:
                if message.from_user.id == id_acc[m]:
                    if (mode_rule[m]=="Answer" or mode_rule[m]=="Basic") and mode_temp == "None":
                        if message.text is None:
                            print("idm")
                            await asyncio.sleep(0.5)
                            await client.send_message(chat_id=id_bot, text="/idm_"+str(message.message_id))
                        else:
                            if message.text[:1] != "/":
                                print("idm")
                                await asyncio.sleep(0.5)
                                await client.send_message(chat_id=id_bot, text="/idm_"+str(message.message_id))
                    return
                if message.from_user.id == id_bot:    
                    if mode_temp == "ApplyBasic":
                        print('N',m)
                        print(answer_list[m])
                        print(layout[m])
                        print('Add basic message id', message.message_id)
                        print(answer_list[m][layout[m]][1])
                        answer_list[m][layout[m]][1][0].append(message.message_id)
                    if mode_temp == "ApplyMessage":
                        print('Add message id', message.message_id)
                        answer_list[m][layout[m]][1][-1].append(message.message_id)

async def hello(client, message):
    global accounts, mode, code, id_bot, phonehash,select_id, phonenumber, hash, id, layout, proxyb, proxyc, id_user_registration, mybot, input_tokken, settings_templates, id_creator_templates, mode_temp, id_user, level_users, mode_rule
    if not (message.text is None) or mode_temp == "Answer" or mode_temp == "Basic":
        if id_user_registration==message.chat.id:     
            print("Rm")
            if mode==5:
                try:
                    await accounts[len(accounts)-1].check_password(message.text)
                except RPCError as e:
                    print(e)
                    await message.reply("Ошибка входа! Введите номер телефона аккаунта")
                    id_user_registration=0
                    return
                else:
                    await success_login(len(accounts)-1,message)
                    return
                return

            if mode==4:
                try:
                    code=message.text[1:-1]
                    await accounts[len(accounts)-1].sign_in(phone_number=phonenumber,phone_code_hash=phonehash,phone_code=code)
                except SessionPasswordNeeded:
                    await message.reply("Введите пароль аккаунта")
                    mode+=1
                except Exception as e:
                    await message.reply("Ошибка")
                    accounts.remove(accounts[len(accounts)-1])
                    print(e)
                    mode=0
                    id_user_registration=0
                else: 
                    await success_login(len(accounts)-1,message)
                    mode=0
                    return
                return

            if mode==3:
                if not proxyb:
                    accounts.append(Client("account"+str(len(accounts)), api_id=id[select_id], api_hash=hash[select_id], proxy=None))
                    await accounts[len(accounts)-1].connect()
                phonenumber=message.text
                print("Телефон: " + phonenumber)
                try:
                    phonehash= (await (accounts[len(accounts)-1].send_code(phonenumber))).phone_code_hash
                except Exception as e:
                    await message.reply("Ошибка")
                    accounts.remove(accounts[len(accounts)-1])
                    print(e)
                    mode+=1
                    id_user_registration=0
                else: 
                    await message.reply("Введите код в формате 0ХХХХХ0, где ХХХХХ - одноразовый код")
                    mode+=1
                return

            if message.text == "/without_proxy":
                accounts.remove(accounts[len(accounts)-1])
                proxyb=False
                mode+=1
                return
            
            if message.text=="/try":
                try:
                    await message.reply("Пробую подключиться...")
                    await accounts[len(accounts)-1].connect()
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
                        accounts.append(Client("account"+str(len(accounts)), api_id=id[select_id], api_hash=hash[select_id], proxy=proxyc))
                        await message.reply("Пробую подключиться...")
                        await accounts[-1].connect()
                    else:
                        if len(message.text.split(" ")) == 4:
                            proxyc = dict(
                                hostname=message.text.split(" ")[0],
                                port=int(message.text.split(" ")[1]),
                                username=message.text.split(" ")[2],
                                password=message.text.split(" ")[3]
                            )
                            accounts.append(Client("account"+str(len(accounts)), api_id=id[select_id], api_hash=hash[select_id], proxy=proxyc))
                            await message.reply("Пробую подключиться...")
                            await accounts[-1].connect()
                            
                        else:
                            await message.reply("Невозможно распознать! Начать с начала? /start")
                            return


                except Exception as e:
                    print(e)
                    await message.reply( "Произошла ошибка! Повторить попытку? /try\nЛибо ведите другие hostname и порт\n/without_proxy – подключиться без прокси")
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
        
        if message.text=="/help":
            await help_message(message)
            return
        
        if message.text == "/hard_reset":
            await message.reply("Сброс аккаунтов!")
            ClearAll()
            return
        
        if message.chat.id in id_acc:
            n = id_acc.index(message.chat.id)      
            print('Mode',mode_temp)
            if message.text == "/create_template" and mode_temp=="None":
                id_creator_templates=message.chat.id
                await message.reply("Введите название шаблона настроек")
                mode_temp="Name"
                return
                
            if id_creator_templates==message.chat.id:
                # print(mode_temp)
                if message.text == "/next":
                    mode_temp="Keyword"
                    settings_templates[-1][-1][1].append([])
                    settings_templates[-1][-1][2].append([])
                    await message.reply("Введите ключевое слово\n/next_rule – следующее правило \n/save – сохранить шаблон")
                    print(settings_templates)
                    return
                
                if message.text == "/next_rule":
                    mode_temp="Basic"
                    settings_templates[-1][-1][1].pop(-1)
                    settings_templates[-1][-1][2].pop(-1)
                    settings_templates[-1].append([[],[[]],[[]]])
                    await message.reply("Введите основное сообщение")
                    print("New rule")
                    return
                
                if message.text == "/save":
                    mode_temp="None"
                    settings_templates[-1][-1][1].pop(-1)
                    settings_templates[-1][-1][2].pop(-1)
                    await message.reply("Шаблон сохранен с названием: " + settings_templates[-1][0] + "\nЧтобы применить шаблон, введите: /apply_"+settings_templates[-1][0])
                    id_creator_templates=0
                    SaveTemplate()
                    return
                
                if mode_temp == "Name":
                    settings_templates.append([message.text.lower(), id_creator_templates, [[],[[]],[[]]]])
                    mode_temp = "Basic"
                    await message.reply("Введите основное сообщение 1-го правила")
                    print(settings_templates)
                    return
            
                if mode_temp == "Basic":
                    settings_templates[-1][-1][1][0].append(message.message_id)
                    await message.reply("Введите время таймаута отправки(сек)")
                    
                    mode_temp="TimeB"
                    return
                
                if mode_temp=="TimeB":
                    try:
                        settings_templates[-1][-1][2][0].append(int(message.text))
                        mode_temp = "Basic"
                        print(settings_templates)
                        await message.reply("Введите следующее основное сообщение или введите /next")
                    except Exception as e:
                        print(e)
                        await message.reply("Ошибка, повторно введите число")
                    return
                
                if mode_temp=="TimeA":
                    try:
                        settings_templates[-1][-1][2][-1].append(int(message.text))
                        await message.reply("Введите следующее сообщение\n/next – далее")
                        mode_temp = "Answer"
                        print(settings_templates)
                    except Exception as e:
                        print(e)
                        await message.reply("Ошибка, повторно введите число")
                    return
                
                if mode_temp == "Keyword":
                    mode_temp="Answer"
                    settings_templates[-1][-1][0].append(message.text.lower())
                    await message.reply("Введите ответ")
                    print(settings_templates)
                    return
                
                if mode_temp == "Answer":
                    mode_temp = "TimeA"
                    settings_templates[-1][-1][1][-1].append(message.message_id)
                    await message.reply("Введите время таймаута отправки(сек)")
                    print(settings_templates)
                    return

            if message.text[:7]=="/apply_":
                if mode_temp=="None":
                    name = message.text[7:]
                    print(name)
                    for i in range(len(settings_templates)):
                        if settings_templates[i][0] == name:
                            await ApplyMessage(client,message,id,i,n)
                            return
                    await message.reply("Шаблон не найден")
                return
            
            if message.text[:6]=="/apply":
                answ="Выберите шаблон:\n"
                for i in range(len(settings_templates)):
                    answ+='/apply_' + settings_templates[i][0] +'\n'
                await message.reply(answ)
                return
            
            if message.text[:16]=="/delete_template":
                answ="Выберите шаблон:\n"
                for i in range(len(settings_templates)):
                    answ+='/del_' + settings_templates[i][0] +'\n'
                await message.reply(answ)
                return
            
            if message.text[:5]=="/del_":
                for i in range(len(settings_templates)):
                    if message.text[5:]==settings_templates[i][0]:
                        settings_templates.pop(i)
                        print(settings_templates)
                        await message.reply('Шаблон ' + message.text[5:] + ' успешно удален!')
                        SaveTemplate()
                        return
                await message.reply('Шаблон не найден!')
                return
            
            if message.text == "/clear_user_history":
                id_user=[]
                level_users=[]
                for i in range(len(accounts)):
                    id_user.append([])
                    level_users.append([])
                SaveUsers()
                print('Users', id_user)
                await message.reply('Прогресс пользователей сброшен!')
                return
            
            if message.text == "/create_rule":
                mode_rule[n]="Basic"
                answer_list[n] = []
                layout[n] = 0
                await message.reply("Введите основное сообщение 1 правила")
                return
            
            if message.text == "/new_rules":
                answer_list[n] = []
                mode_rule[n]="Basic"
                layout[n] = 0
                await message.reply("Правила очищены, введите основное сообщение")
                SaveAnswer()
                return
            
            if message.text == "/next_rule":
                layout[n] += 1
                mode_rule[n]="Basic"
                await message.reply("Правило " + str(layout[n]) + ". Введите основную фразу:")
                return
            
            if input_tokken:
                f=open(resource_path('bot_settings.ini'),'w', encoding='utf-8')     
                f.write("tokken="+message.text)
                f.close()
                await message.reply("Смена бота...")
                print("change bot to: " + message.text)
                input_tokken=False 
                print()
                id_bot=mybot.get_me().id
                print(id_bot)
                # if os.path.isfile("account"+str(n)+".session"):
                #         os.remove(mybot.session_name + ".session")
                os.execv(sys.executable, ['python'] + sys.argv)
                return
                
            if message.text == "/set_tokken":
                await message.reply("Введите токкен бота")
                input_tokken=True
                return

            if message.text == "/next":
                mode_rule[n]="Keyword"
                await message.reply("Введите ключевые слова\nили команду /next_rule")
                return
            await asyncio.sleep(2)

            if message.text[:5] == "/idm_":
                layout[n]
                if len(answer_list[n]) <= layout[n]:
                    answer_list[n].append([[""], [[int(message.text[5:])]], [[]]])
                    mode_rule[n]="TimeB"
                    print("New layout")
                else:
                    if mode_rule[n]=="Basic":
                        answer_list[n][layout[n]][1][0].append(int(message.text[5:]))
                        mode_rule[n]="TimeB"
                    else:
                        answer_list[n][layout[n]][1][-1].append(int(message.text[5:]))
                        mode_rule[n]="TimeA"
                await message.reply('Введите время задержки ответа(сек)')
                print(answer_list)
                return
            
            print("Message to the bot")
            print('N:',n,'Mode:',mode_rule[n])
            if mode_rule[n]=="TimeA":
                mode_rule[n]="Answer"
                answer_list[n][layout[n]][2][-1].append(int(message.text))
                SaveAnswer()
                await message.reply("Введите cледующее сообщение,\n/next – далее")
                return
                
            if mode_rule[n]=="TimeB":
                answer_list[n][layout[n]][2][0].append(int(message.text))
                mode_rule[n]="Basic"
                SaveAnswer()
                await message.reply("Введите следующее основное сообщение\nили команду /next")
                return
                
            if mode_rule[n]=="Keyword":
                answer_list[n][layout[n]][0].append(message.text.lower())
                answer_list[n][layout[n]][1].append([])
                answer_list[n][layout[n]][2].append([])
                mode_rule[n]="Answer"
                await message.reply("Введите ответ:")
                print(answer_list)

def main():
    global mybot, id_bot, accounts, mybot
    bot_setup()
    def_sett()
    openfromfile()
    mybot.add_handler(MessageHandler(hello))
    mybot.start()
    id_bot=mybot.get_me().id
    print("ID bot: " + str(id_bot))
    for app in accounts:
        app.start()
    print("The bot is running!")
    idle()
    mybot.stop()
    for app in accounts:
        app.stop()

if __name__ == '__main__':
    try:
        main()
        # asyncio.run(main())
    except Exception as e:
        print(e)  
        time.sleep(15)