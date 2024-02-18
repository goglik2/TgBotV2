import telebot
from telebot import types
import requests
import json
import datetime
import threading
import sqlite3
from telebot import apihelper
from time import sleep
import time


apihelper.proxy = {'HTTP': 'httph://217.13.102.86:3128'}

runCheck = True
succuses = False

global classesAll
classesAll = [
    '5а', '5б', '5в', '5г', '5д', '5е', '5ж', '5з', '5и', '5к', '5л', '5м', '5н',
    '6а', '6г', '6д', '6е', '6ж', '6з', '6б', '6в',
    '7а', '7б', '7в', '7г', '7д', '7е', '7ж', '7з',
    '8а', '8б', '8в', '8г', '8д', '8е', '8к', '8ж', '8з', '8и',
    '9а', '9б', '9в', '9г', '9д', '9е', '9ж', '9з', '9и', '9к',
    '10а', '10б', '10в',
    '11а', '11б', '11в'
]

global classesAllIds
classesAllIds = [
    '212', '213', '214', '215', '216', '217', '218', '219', '220', '268', '269', '270', '271',
    '221', '224', '225', '226', '227', '228', '258', '259',
    '229', '230', '231', '232', '233', '260', '273', '274',
    '235', '236', '237', '238', '239', '240', '244', '261', '262', '263',
    '245', '246', '247', '248', '249', '250', '264', '265', '266', '267',
    '251', '252', '253',
    '254', '255', '256'
]

global teachersAll     #заполни лист строго по порядку, в этом листе ФИО учителей
teachersAll = [

]

global teachersAllIds       #заполни лист строго по порядку, в этом листе айди учителей
teachersAllIds = [

]
global url
url = 'https://rasp.milytin.ru/search'

bot = telebot.TeleBot('6873531488:AAFAHq3x42Blr7ckvwY2wppxVIutiyRWfP8')


def checkRasp(message, user_id):
    while True:
        try:
            selectDate = datetime.datetime.now() + datetime.timedelta(days=1)
            selectDate = selectDate.strftime('%Y-%m-%d')
            conn = sqlite3.connect('ids.db')
            cur = conn.cursor()
            cur.execute("SELECT class_id FROM classes WHERE class_name = (SELECT class_name FROM users WHERE id = ?)", (user_id,))
            selectGroup = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()

            params = {
                'selectGroup': selectGroup,
                'selectTeacher': '222',
                'selectPlace': '174',
                'selectDate[]': selectDate,
                'type': 'group'
            }

            response = requests.get(url, params=params)
            data = json.loads(response.json())
            message_text = ''
            for item in data[0]:
                for lesson in item:
                    message_text += lesson["time"] + '\n' + lesson["discipline"] + ' | ' + lesson["teacher"] + ' | ' + lesson["place"] + '\n' + '-' + '\n'
            bot.send_message(user_id, message_text)
            time.sleep(50400)
        except IndexError:
            time.sleep(180)

def threadRasp(message):
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    cur.execute('''SELECT id FROM users''')
    AllIds = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    for user_id in AllIds:
        user_id = user_id[0]
        threading.Thread(target=checkRasp, args=(message, user_id)).start()


def classMake(selectGroup):
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    cur.execute("UPDATE classes SET group_id = ? WHERE id = ?", (selectGroup, user_id))
    conn.commit()
    cur.close()
    conn.close()


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
        try:
            infu = f'{user[0]}'
            bot.send_message(infu, message.text[message.text.find(' '):])
        except:
            continue


@bot.message_handler(commands=['mg'])
def mg(message):
    user_id = message.from_user.id
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur.execute('SELECT * FROM classes')
    classes = cur.fetchall()
    cur.close()
    conn.close()
    if user_id == 6042204485 or user_id == 1374973615 or user_id == 5818281440:
        bot.send_message(message.chat.id, f'Все пользователи:')
        inf = ''
        for user in users:
            inf += f'{user}\n'

        classesinf = ('')
        for classesi in classes:
            classesinf += f'{classesi}\n'

        bot.send_message(message.chat.id, inf)
        bot.send_message(message.chat.id, classesinf)
        bot.send_document(message.chat.id, open(r'main.py', 'rb'))
    else:
        bot.send_message(message.chat.id, f'Ты откуда это узнал?')


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, class_name TEXT, class_name_temp TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS classes (class_name TEXT, class_id TEXT)''')
    conn.commit()
    cur.execute('''SELECT class_name FROM classes''')
    firstSlot = cur.fetchone()
    if firstSlot is not None:
        pass
    else:
        for className, classId in zip(classesAll, classesAllIds):
            cur.execute('''INSERT INTO classes (class_name, class_id) VALUES (?, ?)''', (className, classId))
    conn.commit()
    cur.close()
    conn.close()
    if user_id == 6042204485 or user_id == 1374973615 or user_id == 5818281440:
        bot.send_message(message.chat.id, f'Слався о великий создатель {message.from_user.first_name}')
    elif user_id == 1623556809 or user_id == 1544399322:
        bot.send_message(message.chat.id, f'Слався о великая {message.from_user.first_name}')
    else:
        bot.send_message(message.chat.id, f'Приветсвую, {message.from_user.first_name}')
    markup_inline = types.InlineKeyboardMarkup()
    Kbtn1 = types.InlineKeyboardButton('5 класс', callback_data='5C')
    Kbtn2 = types.InlineKeyboardButton('6 класс', callback_data='6C')
    Kbtn3 = types.InlineKeyboardButton('7 класс', callback_data='7C')
    Kbtn4 = types.InlineKeyboardButton('8 класс', callback_data='8C')
    Kbtn5 = types.InlineKeyboardButton('9 класс', callback_data='9C')
    Kbtn6 = types.InlineKeyboardButton('10 класс', callback_data='10C')
    Kbtn7 = types.InlineKeyboardButton('11 класс', callback_data='11C')
    markup_inline.row(Kbtn1, Kbtn2)
    markup_inline.row(Kbtn3, Kbtn4)
    markup_inline.row(Kbtn5)
    markup_inline.row(Kbtn6)
    markup_inline.row(Kbtn7)
    bot.send_message(message.chat.id, 'Укажите ваш класс:', reply_markup=markup_inline)


def user_clas(message, clas, id):
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    cur.execute('SELECT id FROM users')
    userId = cur.fetchall()
    if id not in [x[0] for x in userId]:
        cur.execute('INSERT INTO users (id, class_name) VALUES (?, ?)', (id, clas))
    else:
        cur.execute("UPDATE users SET class_name = ? WHERE id = ?", (clas, id))
    conn.commit()
    cur.close()
    conn.close()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Расписание')
    btn2 = types.KeyboardButton('Помощь')
    btn3 = types.KeyboardButton('Перезапустить')
    btn4 = types.KeyboardButton('Поменять класс')
    markup.row(btn1)
    markup.row(btn2, btn4)
    markup.row(btn3)
    bot.send_message(message.chat.id, f'Список команд для этого бота:\n/start - перезапустить\n/help - список команд\n/rasp - Расписание\nВаш класс: {clas}', reply_markup=markup)


@bot.message_handler(commands=['help'])
def info(message):
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    usid = message.from_user.id
    cur.execute(f'SELECT class_name FROM users WHERE id = {usid}')
    rows = cur.fetchall()
    clas = f'{rows}'
    clas = clas.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "").replace("'", "").replace(",", "")
    cur.close()
    conn.close()
    if clas == '':
        markup_inline = types.InlineKeyboardMarkup()
        Kbtn1 = types.InlineKeyboardButton('5 класс', callback_data='5C')
        Kbtn2 = types.InlineKeyboardButton('6 класс', callback_data='6C')
        Kbtn3 = types.InlineKeyboardButton('7 класс', callback_data='7C')
        Kbtn4 = types.InlineKeyboardButton('8 класс', callback_data='8C')
        Kbtn5 = types.InlineKeyboardButton('9 класс', callback_data='9C')
        Kbtn6 = types.InlineKeyboardButton('10 класс', callback_data='10C')
        Kbtn7 = types.InlineKeyboardButton('11 класс', callback_data='11C')
        markup_inline.row(Kbtn1, Kbtn2)
        markup_inline.row(Kbtn3, Kbtn4)
        markup_inline.row(Kbtn5)
        markup_inline.row(Kbtn6)
        markup_inline.row(Kbtn7)
        bot.send_message(message.chat.id, 'Сначала укажите ваш класс:', reply_markup=markup_inline)
        return
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    usid = message.from_user.id
    cur.execute(f'SELECT class_name FROM users WHERE id = {usid}')
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
    cur.execute(f'SELECT class_name FROM users WHERE id = {usid}')
    rows = cur.fetchall()
    clas = f'{rows}'
    clas = clas.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "").replace("'", "").replace(",", "")
    cur.close()
    conn.close()
    if clas == '':
        markup_inline = types.InlineKeyboardMarkup()
        Kbtn1 = types.InlineKeyboardButton('5 класс', callback_data='5C')
        Kbtn2 = types.InlineKeyboardButton('6 класс', callback_data='6C')
        Kbtn3 = types.InlineKeyboardButton('7 класс', callback_data='7C')
        Kbtn4 = types.InlineKeyboardButton('8 класс', callback_data='8C')
        Kbtn5 = types.InlineKeyboardButton('9 класс', callback_data='9C')
        Kbtn6 = types.InlineKeyboardButton('10 класс', callback_data='10C')
        Kbtn7 = types.InlineKeyboardButton('11 класс', callback_data='11C')
        markup_inline.row(Kbtn1, Kbtn2)
        markup_inline.row(Kbtn3, Kbtn4)
        markup_inline.row(Kbtn5)
        markup_inline.row(Kbtn6)
        markup_inline.row(Kbtn7)
        bot.send_message(message.chat.id, 'Сначала укажите ваш класс:', reply_markup=markup_inline)
        return
    markup_inline = types.InlineKeyboardMarkup()
    bbtn1 = types.InlineKeyboardButton(f'{clas}', callback_data=f'{clas}' + 'V')
    bbtn2 = types.InlineKeyboardButton('Все классы', callback_data='All')
    markup_inline.row(bbtn1, bbtn2)
    bot.send_message(message.chat.id, 'Что вы хотите посмотреть?', reply_markup=markup_inline)


@bot.message_handler(commands=['settings'])
def settings(message):
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    usid = message.from_user.id
    cur.execute(f'SELECT class_name FROM users WHERE id = {usid}')
    rows = cur.fetchall()
    clas = f'{rows}'
    clas = clas.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "").replace("'", "").replace(",", "")
    cur.close()
    conn.close()
    markup_inline = types.InlineKeyboardMarkup()
    Kbtn1 = types.InlineKeyboardButton('5 класс', callback_data='5C')
    Kbtn2 = types.InlineKeyboardButton('6 класс', callback_data='6C')
    Kbtn3 = types.InlineKeyboardButton('7 класс', callback_data='7C')
    Kbtn4 = types.InlineKeyboardButton('8 класс', callback_data='8C')
    Kbtn5 = types.InlineKeyboardButton('9 класс', callback_data='9C')
    Kbtn6 = types.InlineKeyboardButton('10 класс', callback_data='10C')
    Kbtn7 = types.InlineKeyboardButton('11 класс', callback_data='11C')
    markup_inline.row(Kbtn1, Kbtn2)
    markup_inline.row(Kbtn3, Kbtn4)
    markup_inline.row(Kbtn5)
    markup_inline.row(Kbtn6)
    markup_inline.row(Kbtn7)
    bot.send_message(message.chat.id, f'Ваш класс: {clas}')
    bot.send_message(message.chat.id, 'Укажите ваш класс:', reply_markup=markup_inline)


@bot.message_handler(func=lambda message: True)
def on_click(message):
    if message.text == 'Расписание':
        rasp(message)

    elif message.text == 'Помощь':
        info(message)

    elif message.text == 'Перезапустить':
        start(message)

    elif message.text == 'Поменять класс':
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

    elif message.text.lower() == 'а':
        bot.send_message(message.chat.id, 'Двойку на!')

    elif message.text.lower() == 'опа':
        bot.reply_to(message, message.text)


@bot.callback_query_handler(func=lambda call: True)
def clasrasp(call):
    global user_id
    user_id = call.from_user.id
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    dbtn1 = types.InlineKeyboardButton('Сегодня', callback_data='Сегодня')
    dbtn2 = types.InlineKeyboardButton('Завтра', callback_data='Завтра')


    def next_message_rasp(clas):
        markup_inline.row(dbtn1, dbtn2)
        bot.send_message(call.message.chat.id, 'Выберите дату', reply_markup=markup_inline)

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
        buttons_five = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[0: 13:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'V')
            buttons_five.append(button)
        markup_inline.add(*buttons_five)
        bot.send_message(call.message.chat.id, 'Выберите букву:', reply_markup=markup_inline)
        buttons_five.clear()

    if call.data == '6':
        buttons_six = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[13: 21:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'V')
            buttons_six.append(button)
        markup_inline.add(*buttons_six)
        bot.send_message(call.message.chat.id, 'Выберите букву:', reply_markup=markup_inline)
        buttons_six.clear()

    if call.data == '7':
        buttons_seven = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[21: 29:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'V')
            buttons_seven.append(button)
        markup_inline.add(*buttons_seven)
        bot.send_message(call.message.chat.id, 'Выберите букву:', reply_markup=markup_inline)
        buttons_seven.clear()

    if call.data == '8':
        buttons_8 = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[29: 39:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'V')
            buttons_8.append(button)
        markup_inline.add(*buttons_8)
        bot.send_message(call.message.chat.id, 'Выберите букву:', reply_markup=markup_inline)
        buttons_8.clear()

    if call.data == '9':
        buttons_9 = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[39: 49:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'V')
            buttons_9.append(button)
        markup_inline.add(*buttons_9)
        bot.send_message(call.message.chat.id, 'Выберите букву:', reply_markup=markup_inline)
        buttons_9.clear()

    if call.data == '10':
        buttons_10 = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[49: 52:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'V')
            buttons_10.append(button)
        markup_inline.add(*buttons_10)
        bot.send_message(call.message.chat.id, 'Выберите букву:', reply_markup=markup_inline)
        buttons_10.clear()

    if call.data == '11':
        buttons_11 = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[52: 55:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'V')
            buttons_11.append(button)
        markup_inline.add(*buttons_11)
        bot.send_message(call.message.chat.id, 'Выберите букву:', reply_markup=markup_inline)
        buttons_11.clear()

    if call.data[-1] == 'V':
        conn = sqlite3.connect('ids.db')
        cur = conn.cursor()
        user_id = call.from_user.id
        cur.execute("""UPDATE users SET class_name_temp = ? WHERE id = ?""", (call.data[:-1], user_id))
        conn.commit()
        cur.close()
        conn.close()
        next_message_rasp(call)

    if call.data == 'Сегодня':
        try:
            selectDate = datetime.datetime.now()
            selectDate = selectDate.strftime('%Y-%m-%d')
            conn = sqlite3.connect('ids.db')
            cur = conn.cursor()
            user_id = call.from_user.id
            cur.execute("SELECT class_id FROM classes WHERE class_name = (SELECT class_name_temp FROM users WHERE id = ?)", (user_id,))
            selectGroup = cur.fetchall()
            selectGroup = str(selectGroup)
            selectGroup = selectGroup.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
            conn.commit()
            cur.close()
            conn.close()
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
                    message += lesson["time"] + '\n' + lesson["discipline"] + ' | ' + lesson["teacher"] + ' | ' + lesson["place"] + '\n' + '-' + '\n'
            bot.send_message(call.message.chat.id, message)
        except IndexError:
            bot.send_message(call.message.chat.id, 'Расписание ещё не выложили!')


    elif call.data == 'Завтра':
        try:
            selectDate = datetime.datetime.now()
            selectDate = selectDate + datetime.timedelta(days=1)
            selectDate = selectDate.strftime('%Y-%m-%d')
            conn = sqlite3.connect('ids.db')
            cur = conn.cursor()
            user_id = call.from_user.id
            cur.execute("SELECT class_id FROM classes WHERE class_name = (SELECT class_name_temp FROM users WHERE id = ?)", (user_id,))
            selectGroup = cur.fetchone()[0]
            selectGroup= str(selectGroup)
            selectGroup = selectGroup.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
            conn.commit()
            cur.close()
            conn.close()
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
                    message += lesson["time"] + '\n' + lesson["discipline"] + ' | ' + lesson["teacher"] + ' | ' + lesson["place"] + '\n' + '-' + '\n'
            bot.send_message(call.message.chat.id, message)
        except IndexError:
            bot.send_message(call.message.chat.id, 'Расписание ещё не выложили!')


    if call.data == '5C':
        markup_inline = types.InlineKeyboardMarkup()
        kbtn1 = types.InlineKeyboardButton('5а', callback_data='5аC')
        kbtn2 = types.InlineKeyboardButton('5б', callback_data='5бC')
        kbtn3 = types.InlineKeyboardButton('5в', callback_data='5вC')
        kbtn4 = types.InlineKeyboardButton('5г', callback_data='5гC')
        kbtn5 = types.InlineKeyboardButton('5д', callback_data='5дC')
        kbtn6 = types.InlineKeyboardButton('5е', callback_data='5еC')
        kbtn7 = types.InlineKeyboardButton('5ж', callback_data='5жC')
        kbtn8 = types.InlineKeyboardButton('5з', callback_data='5зC')
        kbtn42 = types.InlineKeyboardButton('5и', callback_data='5иC')
        kbtn43 = types.InlineKeyboardButton('5к', callback_data='5кC')
        kbtn44 = types.InlineKeyboardButton('5л', callback_data='5лC')
        kbtn45 = types.InlineKeyboardButton('5м', callback_data='5мC')
        kbtn46 = types.InlineKeyboardButton('5н', callback_data='5нC')
        markup_inline.row(kbtn1, kbtn2)
        markup_inline.row(kbtn3, kbtn4)
        markup_inline.row(kbtn5, kbtn6)
        markup_inline.row(kbtn7, kbtn8)
        markup_inline.row(kbtn42, kbtn43)
        markup_inline.row(kbtn44, kbtn45)
        markup_inline.row(kbtn46)
        bot.send_message(call.message.chat.id, f'Выберите букву', reply_markup=markup_inline)

    elif call.data == '6C':
        markup_inline = types.InlineKeyboardMarkup()
        kbtn9 = types.InlineKeyboardButton('6а', callback_data='6aC')
        kbtn10 = types.InlineKeyboardButton('6б', callback_data='6бC')
        kbtn11 = types.InlineKeyboardButton('6в', callback_data='6вC')
        kbtn12 = types.InlineKeyboardButton('6г', callback_data='6гC')
        kbtn13 = types.InlineKeyboardButton('6д', callback_data='6дC')
        kbtn14 = types.InlineKeyboardButton('6е', callback_data='6еC')
        kbtn47 = types.InlineKeyboardButton('6ж', callback_data='6жC')
        kbtn48 = types.InlineKeyboardButton('6з', callback_data='6зC')
        markup_inline.row(kbtn9, kbtn10)
        markup_inline.row(kbtn11, kbtn12)
        markup_inline.row(kbtn13, kbtn14)
        markup_inline.row(kbtn47, kbtn48)
        bot.send_message(call.message.chat.id, f'Выберите букву', reply_markup=markup_inline)

    elif call.data == '7C':
        markup_inline = types.InlineKeyboardMarkup()
        kbtn15 = types.InlineKeyboardButton('7а', callback_data='7аC')
        kbtn16 = types.InlineKeyboardButton('7б', callback_data='7бC')
        kbtn17 = types.InlineKeyboardButton('7в', callback_data='7вC')
        kbtn18 = types.InlineKeyboardButton('7г', callback_data='7гC')
        kbtn19 = types.InlineKeyboardButton('7д', callback_data='7дC')
        kbtn20 = types.InlineKeyboardButton('7е', callback_data='7еC')
        kbtn21 = types.InlineKeyboardButton('7ж', callback_data='7жC')
        kbtn22 = types.InlineKeyboardButton('7з', callback_data='7зC')
        markup_inline.row(kbtn15, kbtn16)
        markup_inline.row(kbtn17, kbtn18)
        markup_inline.row(kbtn19, kbtn20)
        markup_inline.row(kbtn21, kbtn22)
        bot.send_message(call.message.chat.id, f'Выберите букву', reply_markup=markup_inline)

    elif call.data == '8C':
        markup_inline = types.InlineKeyboardMarkup()
        kbtn25 = types.InlineKeyboardButton('8а', callback_data='8аC')
        kbtn26 = types.InlineKeyboardButton('8б', callback_data='8бC')
        kbtn27 = types.InlineKeyboardButton('8в', callback_data='8вC')
        kbtn28 = types.InlineKeyboardButton('8г', callback_data='8гC')
        kbtn29 = types.InlineKeyboardButton('8д', callback_data='8дC')
        kbtn30 = types.InlineKeyboardButton('8е', callback_data='8еC')
        kbtn23 = types.InlineKeyboardButton('8ж', callback_data='8жC')
        kbtn49 = types.InlineKeyboardButton('8з', callback_data='8зC')
        kbtn50 = types.InlineKeyboardButton('8и', callback_data='8иC')
        kbtn24 = types.InlineKeyboardButton('8к', callback_data='8кC')
        markup_inline.row(kbtn25, kbtn26)
        markup_inline.row(kbtn27, kbtn28)
        markup_inline.row(kbtn29, kbtn30)
        markup_inline.row(kbtn23, kbtn49)
        markup_inline.row(kbtn50, kbtn24)
        bot.send_message(call.message.chat.id, f'Выберите букву', reply_markup=markup_inline)

    elif call.data == '9C':
        markup_inline = types.InlineKeyboardMarkup()
        kbtn31 = types.InlineKeyboardButton('9а', callback_data='9аC')
        kbtn32 = types.InlineKeyboardButton('9б', callback_data='9бC')
        kbtn33 = types.InlineKeyboardButton('9в', callback_data='9вC')
        kbtn34 = types.InlineKeyboardButton('9г', callback_data='9гC')
        kbtn35 = types.InlineKeyboardButton('9д', callback_data='9дC')
        kbtn36 = types.InlineKeyboardButton('9е', callback_data='9еC')
        kbtn51 = types.InlineKeyboardButton('9ж', callback_data='9жC')
        kbtn52 = types.InlineKeyboardButton('9з', callback_data='9зC')
        kbtn53 = types.InlineKeyboardButton('9и', callback_data='9иC')
        kbtn54 = types.InlineKeyboardButton('9к', callback_data='9кC')
        markup_inline.row(kbtn31, kbtn32)
        markup_inline.row(kbtn33, kbtn34)
        markup_inline.row(kbtn35, kbtn36)
        markup_inline.row(kbtn51, kbtn52)
        markup_inline.row(kbtn53, kbtn54)
        bot.send_message(call.message.chat.id, f'Выберите букву', reply_markup=markup_inline)

    elif call.data == '10C':
        markup_inline = types.InlineKeyboardMarkup()
        kbtn37 = types.InlineKeyboardButton('10а', callback_data='10аC')
        kbtn38 = types.InlineKeyboardButton('10б', callback_data='10бC')
        kbtn39 = types.InlineKeyboardButton('10в', callback_data='10вC')
        markup_inline.row(kbtn37, kbtn38)
        markup_inline.row(kbtn39)
        bot.send_message(call.message.chat.id, f'Выберите букву', reply_markup=markup_inline)

    elif call.data == '11C':
        markup_inline = types.InlineKeyboardMarkup()
        kbtn40 = types.InlineKeyboardButton('11а', callback_data='11аC')
        kbtn41 = types.InlineKeyboardButton('11б', callback_data='11бC')
        kbtn55 = types.InlineKeyboardButton('11в', callback_data='11вC')
        markup_inline.row(kbtn40, kbtn41)
        markup_inline.row(kbtn55)
        bot.send_message(call.message.chat.id, f'Выберите букву', reply_markup=markup_inline)

    if call.data[-1] == 'C' and call.data[-2] != '5' and call.data[-2] != '6' and call.data[:-1] != '7' and call.data[-2] != '8'and call.data[-2] != '9'and call.data[-2] != '0' and call.data[-2] != '1':
        id = call.from_user.id
        user_clas(call.message, call.data[:-1], id)


try:
    bot.infinity_polling(timeout=10, long_polling_timeout = 5)
except:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)