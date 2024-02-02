import telebot
from telebot import types
import requests
import json
import datetime
import time
import threading
import sqlite3

global url
url = 'https://rasp.milytin.ru/search'

bot = telebot.TeleBot('6741433926:AAGJrOgChrNOZgZfU0JWssuN1Y-ws_3s7LI')

def checkrasp(message):
    while True:
        try:
            selectDate = datetime.datetime.now()
            selectDate = selectDate + datetime.timedelta(days=1)
            selectDate = selectDate.strftime('%Y-%m-%d')
            selectDate = f'{selectDate}'
            url = 'https://rasp.milytin.ru/search'
            params = {
                'selectGroup': '248',
                'selectTeacher': '222',
                'selectPlace': '174',
                'selectDate[]': selectDate,
                'type': 'group'
            }
            response = requests.get(url, params=params)
            data_str = response.json()
            data = json.loads(data_str)
            conn = sqlite3.connect('ids.db')
            cur = conn.cursor()
            cur.execute('SELECT * FROM users')
            users = cur.fetchall()
            cur.close()
            conn.close()
            infu = ''
            for user in users:
                infu = f'{user[0]}'
                bot.send_message(infu, 'Расписание обновилось!')
            time.sleep(43200)
        except IndexError:
            time.sleep(300)


def startthread(message):
    thread = threading.Thread(target=checkrasp(message), args=(message))
    thread.start()

@bot.message_handler(commands=['startcheck'])
def startcheckraspcheck(message):
    startthread(message)

@bot.message_handler(commands=['post23'])
def post(message):
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()
    infu = ''
    for user in users:
        infu = f'{user[0]}'
        bot.send_message(infu, message.text[message.text.find(' '):])


@bot.message_handler(commands=['mg'])
def mg(message):
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f'Все пользователи:')
    inf = ''
    for user in users:
        inf += f'{user}\n'

    bot.send_message(message.chat.id, inf)
    bot.send_document(message.chat.id, open(r'main.py', 'rb'))


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, clas TEXT)')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f'Приветсвую, {message.from_user.first_name}')
    bot.send_message(message.chat.id, f'Список команд для этого бота:\n/start - перезапустить\n/help - список команд\n/rasp - Расписание')
    bot.send_message(message.chat.id, 'Введите ваш класс, например 5а или 9г:')
    bot.register_next_step_handler(message, user_clas)

def user_clas(message):
    name = message.from_user.first_name
    global clas
    global id
    id = message.from_user.id
    clas = message.text.strip().lower()
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    cur.execute('SELECT id FROM users')
    userId = cur.fetchall()
    if id not in [x[0] for x in userId]:
        cur.execute('INSERT INTO users (id, name, clas) VALUES (?, ?, ?)', (id, name, clas))
    else:
        cur.execute('UPDATE users SET clas = ? WHERE id = ?', (clas, id))
    conn.commit()
    cur.close()
    conn.close()
    clas = message.text.strip().lower()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Расписание')
    btn2 = types.KeyboardButton('Помощь')
    btn3 = types.KeyboardButton('Перезапустить')
    btn4 = types.KeyboardButton('Настройки')
    markup.row(btn1)
    markup.row(btn2, btn4)
    markup.row(btn3)
    bot.send_message(message.chat.id, f'Ваш класс: {clas}', reply_markup=markup)


@bot.message_handler(commands=['help'])
def info(message):
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    usid = message.from_user.id
    cur.execute(f'SELECT clas FROM users WHERE id = {usid}')
    rows = cur.fetchall()
    clas = f'{rows}'
    clas = clas.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "").replace("'", "").replace(",", "")
    cur.close()
    conn.close()
    if clas == '':
        bot.send_message(message.chat.id, 'Сначала укажите ваш класс')
        bot.register_next_step_handler(message, user_clas)
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    usid = message.from_user.id
    cur.execute(f'SELECT clas FROM users WHERE id = {usid}')
    rows = cur.fetchall()
    clas = f'{rows}'
    clas = clas.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "").replace("'", "").replace(",", "")
    cur.close()
    conn.close()
    bot.send_message(message.chat.id,f'Ваш класс: {clas}\nСписок команд для этого бота:\n/start - перезапустить\n/help - список команд\n/settings - поменять класс\n/rasp - Расписание')

@bot.message_handler(commands=['rasp'])
def rasp(message):
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    usid = message.from_user.id
    cur.execute(f'SELECT clas FROM users WHERE id = {usid}')
    rows = cur.fetchall()
    clas = f'{rows}'
    clas = clas.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "").replace("'", "").replace(",", "")
    cur.close()
    conn.close()
    if clas == '':
        bot.send_message(message.chat.id, 'Сначала укажите ваш класс')
        bot.register_next_step_handler(message, user_clas)
    markup_inline = types.InlineKeyboardMarkup()
    bbtn1 = types.InlineKeyboardButton(f'{clas}', callback_data=f'{clas}')
    bbtn2 = types.InlineKeyboardButton('Все классы', callback_data='All')
    markup_inline.row(bbtn1, bbtn2)
    bot.send_message(message.chat.id, 'Что вы хотите посмотреть?', reply_markup=markup_inline)

@bot.message_handler(commands=['settings'])
def settings(message):
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    usid = message.from_user.id
    cur.execute(f'SELECT clas FROM users WHERE id = {usid}')
    rows = cur.fetchall()
    clas = f'{rows}'
    clas = clas.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "").replace("'", "").replace(",", "")
    cur.close()
    conn.close()
    if clas == '':
        bot.send_message(message.chat.id, 'Сначала укажите ваш класс')
        bot.register_next_step_handler(message, user_clas)
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    usid = message.from_user.id
    cur.execute(f'SELECT clas FROM users WHERE id = {usid}')
    rows = cur.fetchall()
    clas = f'{rows}'
    clas = clas.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "").replace("'",
                                                                                                             "").replace(
        ",", "")
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f'Ваш класс: {clas}\nВведите ваш класс, например 5а или 9г:')
    bot.register_next_step_handler(message, user_clas)

@bot.message_handler(func=lambda message: True)
def on_click(message):
    if message.text == 'Расписание':
        rasp(message)

    elif message.text == 'Помощь':
        info(message)

    elif message.text == 'Перезапустить':
        start(message)

    elif message.text == 'Настройки':
        settings(message)

    elif message.text.lower() == 'разработчик':
        bot.send_message(message.chat.id, 'Сие творение создал Григорий и моральную помощь оказывал его юный подаван Владимир\nГригорий: @FIVE_HH, 89110483340(кому не сложно скиньте денег)\nВладимир: @Discketaa, 89216874164\nЕсли вы увидели это сообщение, то обязаны нам написать или позвонить!')

    elif message.text.lower() == 'нет':
        bot.send_message(message.chat.id, 'пятиклассника ответ!')

    elif message.text.lower() == 'капибара':
        bot.send_message(message.chat.id, 'Что?')

    elif message.text.lower() == 'утюг':
        bot.send_message(message.chat.id, 'Причём это тут?')

    elif message.text.lower() == 'уксус':
        bot.send_message(message.chat.id, 'Ладно...')

    elif message.text.lower() == 'женщина':
        bot.send_message(message.chat.id, 'Где!')

    elif message.text.lower() == 'девушка':
        bot.send_message(message.chat.id, 'Где!')

    elif message.text.lower() == 'владимир путин':
        bot.send_message(message.chat.id, 'Молодец!\nПолитик, лидер и боец!')

    elif message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'привет')

    elif message.text.lower() == 'великолепно':
        bot.send_message(message.chat.id, 'В этот великолепный день, доделался этот великолепный бот, как-же это великолепно!')

@bot.callback_query_handler(func=lambda call: True)
def clasrasp(call):
    global selectGroup
    markup_inline = types.InlineKeyboardMarkup()
    dbtn1 = types.InlineKeyboardButton('Сегодня', callback_data='Сегодня')
    dbtn2 = types.InlineKeyboardButton('Завтра', callback_data='Завтра')
    if call.data == 'All':
        kbtn42 = types.InlineKeyboardButton('5 класс', callback_data='5')
        kbtn43 = types.InlineKeyboardButton('6 класс', callback_data='6')
        kbtn44 = types.InlineKeyboardButton('7 класс', callback_data='7')
        kbtn45 = types.InlineKeyboardButton('8 класс', callback_data='8')
        kbtn46 = types.InlineKeyboardButton('9 класс', callback_data='9')
        kbtn47 = types.InlineKeyboardButton('10 класс', callback_data='10')
        kbtn48 = types.InlineKeyboardButton('11 класс', callback_data='11')
        markup_inline.row(kbtn42, kbtn43)
        markup_inline.row(kbtn44, kbtn45)
        markup_inline.row(kbtn46)
        markup_inline.row(kbtn47)
        markup_inline.row(kbtn48)
        bot.send_message(call.message.chat.id, 'Выберите класс:', reply_markup= markup_inline)

    if call.data == '5':
        markup_inline = types.InlineKeyboardMarkup()
        kbtn1 = types.InlineKeyboardButton('5а', callback_data='5а')
        kbtn2 = types.InlineKeyboardButton('5б', callback_data='5б')
        kbtn3 = types.InlineKeyboardButton('5в', callback_data='5в')
        kbtn4 = types.InlineKeyboardButton('5г', callback_data='5г')
        kbtn5 = types.InlineKeyboardButton('5д', callback_data='5д')
        kbtn6 = types.InlineKeyboardButton('5е', callback_data='5е')
        kbtn7 = types.InlineKeyboardButton('5ж', callback_data='5ж')
        kbtn8 = types.InlineKeyboardButton('5з', callback_data='5з')
        kbtn42 = types.InlineKeyboardButton('5и', callback_data='5и')
        kbtn43 = types.InlineKeyboardButton('5к', callback_data='5к')
        kbtn44 = types.InlineKeyboardButton('5л', callback_data='5л')
        kbtn45 = types.InlineKeyboardButton('5м', callback_data='5м')
        kbtn46 = types.InlineKeyboardButton('5н', callback_data='5н')
        markup_inline.row(kbtn1, kbtn2)
        markup_inline.row(kbtn3, kbtn4)
        markup_inline.row(kbtn5, kbtn6)
        markup_inline.row(kbtn7, kbtn8)
        markup_inline.row(kbtn42, kbtn43)
        markup_inline.row(kbtn44, kbtn45)
        markup_inline.row(kbtn46)
        bot.send_message(call.message.chat.id, f'Выберите букву', reply_markup = markup_inline)


    elif call.data == '6':
        markup_inline = types.InlineKeyboardMarkup()
        kbtn9 = types.InlineKeyboardButton('6а', callback_data='6a')
        kbtn10 = types.InlineKeyboardButton('6б', callback_data='6б')
        kbtn11 = types.InlineKeyboardButton('6в', callback_data='6в')
        kbtn12 = types.InlineKeyboardButton('6г', callback_data='6г')
        kbtn13 = types.InlineKeyboardButton('6д', callback_data='6д')
        kbtn14 = types.InlineKeyboardButton('6е', callback_data='6е')
        kbtn47 = types.InlineKeyboardButton('6ж', callback_data='6ж')
        kbtn48 = types.InlineKeyboardButton('6з', callback_data='6з')
        markup_inline.row(kbtn9, kbtn10)
        markup_inline.row(kbtn11, kbtn12)
        markup_inline.row(kbtn13, kbtn14)
        markup_inline.row(kbtn47, kbtn48)
        bot.send_message(call.message.chat.id, f'Выберите букву', reply_markup = markup_inline)

    elif call.data == '7':
        markup_inline = types.InlineKeyboardMarkup()
        kbtn15 = types.InlineKeyboardButton('7а', callback_data='7а')
        kbtn16 = types.InlineKeyboardButton('7б', callback_data='7б')
        kbtn17 = types.InlineKeyboardButton('7в', callback_data='7в')
        kbtn18 = types.InlineKeyboardButton('7г', callback_data='7г')
        kbtn19 = types.InlineKeyboardButton('7д', callback_data='7д')
        kbtn20 = types.InlineKeyboardButton('7е', callback_data='7е')
        kbtn21 = types.InlineKeyboardButton('7ж', callback_data='7ж')
        kbtn22 = types.InlineKeyboardButton('7з', callback_data='7з')
        markup_inline.row(kbtn15, kbtn16)
        markup_inline.row(kbtn17, kbtn18)
        markup_inline.row(kbtn19, kbtn20)
        markup_inline.row(kbtn21, kbtn22)
        bot.send_message(call.message.chat.id, f'Выберите букву', reply_markup = markup_inline)

    elif call.data == '8':
        markup_inline = types.InlineKeyboardMarkup()
        kbtn25 = types.InlineKeyboardButton('8а', callback_data='8а')
        kbtn26 = types.InlineKeyboardButton('8б', callback_data='8б')
        kbtn27 = types.InlineKeyboardButton('8в', callback_data='8в')
        kbtn28 = types.InlineKeyboardButton('8г', callback_data='8г')
        kbtn29 = types.InlineKeyboardButton('8д', callback_data='8д')
        kbtn30 = types.InlineKeyboardButton('8е', callback_data='8е')
        kbtn23 = types.InlineKeyboardButton('8ж', callback_data='8ж')
        kbtn49 = types.InlineKeyboardButton('8з', callback_data='8з')
        kbtn50 = types.InlineKeyboardButton('8и', callback_data='8и')
        kbtn24 = types.InlineKeyboardButton('8к', callback_data='8к')
        markup_inline.row(kbtn25, kbtn26)
        markup_inline.row(kbtn27, kbtn28)
        markup_inline.row(kbtn29, kbtn30)
        markup_inline.row(kbtn23, kbtn49)
        markup_inline.row(kbtn50, kbtn24)
        bot.send_message(call.message.chat.id, f'Выберите букву', reply_markup = markup_inline)

    elif call.data == '9':
        markup_inline = types.InlineKeyboardMarkup()
        kbtn31 = types.InlineKeyboardButton('9а', callback_data='9а')
        kbtn32 = types.InlineKeyboardButton('9б', callback_data='9б')
        kbtn33 = types.InlineKeyboardButton('9в', callback_data='9в')
        kbtn34 = types.InlineKeyboardButton('9г', callback_data='9г')
        kbtn35 = types.InlineKeyboardButton('9д', callback_data='9д')
        kbtn36 = types.InlineKeyboardButton('9е', callback_data='9е')
        kbtn51 = types.InlineKeyboardButton('9ж', callback_data='9ж')
        kbtn52 = types.InlineKeyboardButton('9з', callback_data='9з')
        kbtn53 = types.InlineKeyboardButton('9и', callback_data='9и')
        kbtn54 = types.InlineKeyboardButton('9к', callback_data='9к')
        markup_inline.row(kbtn31, kbtn32)
        markup_inline.row(kbtn33, kbtn34)
        markup_inline.row(kbtn35, kbtn36)
        markup_inline.row(kbtn51, kbtn52)
        markup_inline.row(kbtn53, kbtn54)
        bot.send_message(call.message.chat.id, f'Выберите букву', reply_markup=markup_inline)

    elif call.data == '10':
        markup_inline = types.InlineKeyboardMarkup()
        kbtn37 = types.InlineKeyboardButton('10а', callback_data='10а')
        kbtn38 = types.InlineKeyboardButton('10б', callback_data='10б')
        kbtn39 = types.InlineKeyboardButton('10в', callback_data='10в')
        markup_inline.row(kbtn37, kbtn38)
        markup_inline.row(kbtn39)
        bot.send_message(call.message.chat.id, f'Выберите букву', reply_markup=markup_inline)

    elif call.data == '11':
        markup_inline = types.InlineKeyboardMarkup()
        kbtn40 = types.InlineKeyboardButton('11а', callback_data='11а')
        kbtn41 = types.InlineKeyboardButton('11б', callback_data='11б')
        kbtn55 = types.InlineKeyboardButton('11в', callback_data='11в')
        markup_inline.row(kbtn40, kbtn41)
        markup_inline.row(kbtn55)
        bot.send_message(call.message.chat.id, f'Выберите букву', reply_markup=markup_inline)

    if call.data == '5а':
        selectGroup = '212'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '5б':
        selectGroup = '213'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '5в':
        selectGroup = '214'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '5г':
        selectGroup = '215'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '5д':
        selectGroup = '216'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '5е':
        selectGroup = '217'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '5ж':
        selectGroup = '218'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '5з':
        selectGroup = '219'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '5и':
        selectGroup = '220'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '5к':
        selectGroup = '268'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '5л':
        selectGroup = '269'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '5м':
        selectGroup = '270'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '5н':
        selectGroup = '271'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '6а':
        selectGroup = '221'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '6г':
        selectGroup = '224'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '6д':
        selectGroup = '225'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '6е':
        selectGroup = '226'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '6ж':
        selectGroup = '227'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '6з':
        selectGroup = '228'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '6б':
        selectGroup = '258'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '6в':
        selectGroup = '259'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '7а':
        selectGroup = '229'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '7б':
        selectGroup = '230'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '7в':
        selectGroup = '231'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '7г':
        selectGroup = '232'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '7д':
        selectGroup = '233'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '7е':
        selectGroup = '260'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '7ж':
        selectGroup = '273'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '7з':
        selectGroup = '274'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '8а':
        selectGroup = '235'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '8б':
        selectGroup = '236'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '8в':
        selectGroup = '237'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '8г':
        selectGroup = '238'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '8д':
        selectGroup = '239'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '8е':
        selectGroup = '240'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '8к':
        selectGroup = '244'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '8ж':
        selectGroup = '261'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '8з':
        selectGroup = '262'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '8и':
        selectGroup = '263'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '9а':
        selectGroup = '245'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '9б':
        selectGroup = '246'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '9в':
        selectGroup = '247'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '9г':
        selectGroup = '248'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '9д':
        selectGroup = '249'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '9е':
        selectGroup = '250'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '9ж':
        selectGroup = '264'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '9з':
        selectGroup = '265'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '9и':
        selectGroup = '266'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '9к':
        selectGroup = '267'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '10а':
        selectGroup = '251'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '10б':
        selectGroup = '252'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '10в':
        selectGroup = '253'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '11а':
        selectGroup = '254'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '11б':
        selectGroup = '255'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    elif call.data == '11в':
        selectGroup = '256'
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

    if call.data == 'Сегодня':
        try:
            selectDate = datetime.datetime.now()
            selectDate = selectDate.strftime('%Y-%m-%d')
            selectDate = f'{selectDate}'
            params = {
                'selectGroup': selectGroup,
                'selectTeacher': '222',
                'selectPlace': '174',
                'selectDate[]': selectDate,
                'type': 'group'
            }
            response = requests.get(url, params=params)
            data_str = response.json()
            data = json.loads(data_str)
            message = ''
            for item in data[0]:
                for lesson in item:
                    message += lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["teacher"] + ' | ' + lesson["place"] + '\n' + '-' + '\n'
            bot.send_message(call.message.chat.id, message)
        except IndexError:
            bot.send_message(call.message.chat.id, 'Расписание ещё не выложили!')


    elif call.data == 'Завтра':
        try:
            selectDate = datetime.datetime.now()
            selectDate = selectDate + datetime.timedelta(days=1)
            selectDate = selectDate.strftime('%Y-%m-%d')
            selectDate = f'{selectDate}'
            params = {
                'selectGroup': selectGroup,
                'selectTeacher': '222',
                'selectPlace': '174',
                'selectDate[]': selectDate,
                'type': 'group'
            }
            response = requests.get(url, params=params)
            data_str = response.json()
            data = json.loads(data_str)
            message = ''
            for item in data[0]:
                for lesson in item:
                    message += lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["teacher"] + ' | ' + lesson["place"] + '\n' + '-' + '\n'
            bot.send_message(call.message.chat.id, message)
        except IndexError:
            bot.send_message(call.message.chat.id, 'Расписание ещё не выложили!')

bot.polling(none_stop=True)