
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from pyrogram import Client, idle
from pyrogram.handlers import MessageHandler
from pyrogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import calendar

CREDENTIALS_FILE = 'creds.json'

spreadsheet_id = '1TmfqOaWMjnRduVXcJViY-YrNYalcn9NnIJMDbXWxFNQ'

def add_row(name_m, count_m, type_m):

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A2:A51',
        majorDimension='COLUMNS'
    ).execute()

    last_row = len(values['values'][0]) + 2
    date_now = f'{date.today().day:02}.{date.today().month:02}'
    
    # type_m = 'INCOME'
    # type_m = 'EXPENSE'

    # print(f'Сегодня {date_now}')
    # print(f'Последняя дата: {last_date}')
    # print(f'Первая пустая ячейка: {last_cell}')
    
    val = [[date_now, name_m]]
    if type_m == 'INCOME':
        val[0].append(count_m)
        val[0].append(0)

    elif type_m == 'EXPENSE':
        val[0].append(0)
        val[0].append(count_m)

    val[0].append(f'=E{last_row - 1}-C{last_row}+D{last_row}')

    data = [
            {"range": 'A' + str(last_row),
            "majorDimension": "ROWS",
            "values": val}
    	    ] 

    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": data
        }
    ).execute()
    
    balance = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='E' + str(last_row),
        majorDimension='COLUMNS'
    ).execute()

    return balance['values'][0][0]

def handl(client, message):
    global type_m, summ, input_summ, input_name
    if message.text == '/start':
        message.reply('Что хотите внести?', reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Доход'), KeyboardButton('Расход')]]))
        return

    if message.text == 'Доход':
        type_m = 'EXPENSE'
        message.reply('Введите сумму', reply_markup=ReplyKeyboardRemove())
        input_summ = True
        return

    if message.text == 'Расход':
        type_m = 'INCOME'
        message.reply('Введите сумму', reply_markup=ReplyKeyboardRemove())
        input_summ = True
        return
    
    if input_summ:
        try:
            summ = int(message.text)
        except Exception as e:
            print(e)
            message.reply('Ошибка')
        finally:
            message.reply('Введите название')
            input_summ = False
            input_name = True
            return

    if input_name:
        name_m = message.text
        balance = add_row(name_m, summ, type_m)
        len_month = calendar.monthrange(date.today().year, date.today().month)[1]
        money_for_the_day = round(int(balance)/(len_month - date.today().day))
        print(len_month - date.today().day)
        message.reply(f'Баланс на сегодня: **{balance}**\nДенег на день: **{money_for_the_day}**')
        input_name = False
        return
    

    
    

def main():
    global input_name, input_summ
    input_summ = False
    input_name = False
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
    # balance = add_row('Продукция', 154, 'INCOME')
    # len_month = calendar.monthrange(date.today().year, date.today().month)[1]
    # money_for_the_day = round(int(balance)/len_month)
    # print(f'Баланс: {balance}')
    # print(f'Дней в месяце: {len_month}')
    # print(f'Денег на день: {money_for_the_day}')

if __name__ == '__main__':
    main()