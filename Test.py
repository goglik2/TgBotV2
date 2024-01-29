import telebot
from telebot import types
import requests
import json
import datetime
import time
import threading




bot = telebot.TeleBot('6873531488:AAFAHq3x42Blr7ckvwY2wppxVIutiyRWfP8')

users = []
c_users = 0

joinedFile = open('ids.txt', 'r')
joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()


def checkrasp(chat_id):
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
            bot.send_message(chat_id, 'Расписание обновилось!')
            time.sleep(86400)
        except IndexError:
            time.sleep(150)

with open('ids.txt', 'r') as joinedFile:
    joinedUsers = set(line.strip() for line in joinedFile)

for chat_id in joinedUsers:
    thr = threading.Thread(target=checkrasp, args=(chat_id,))
    thr.start()


@bot.message_handler(commands=['post23'])
def post(message):
    with open('ids.txt', 'r') as file:
        lines = file.readlines()

    unique_lines = set(lines)
    with open('ids.txt', 'w') as file:
        file.writelines(unique_lines)

    for user in joinedUsers:
        bot.send_message(user, message.text[message.text.find(' '):])

@bot.message_handler(commands=['mg'])    #команда только для разработчиков, нужна для просмотра информации о чате и пользователе
def mg(message):
    with open('ids.txt', 'r') as file:
        lines = file.readlines()

    unique_lines = set(lines)
    with open('ids.txt', 'w') as file:
        file.writelines(unique_lines)

    bot.send_message(message.chat.id, message)
    bot.send_message(message.chat.id, f'Все пользователи:')
    for item in users:
        bot.send_message(message.chat.id, f'{item}')

    bot.send_message(message.chat.id, f'Всего пользователей: {c_users}')
    joinedFile = open('ids.txt', 'r')
    bot.send_document(message.chat.id, joinedFile)
    joinedFile.close()

@bot.message_handler(commands=['start'])  #Команда для запуска бота и его стартовой функции
def start(message):
    if not str(message.chat.id) in joinedUsers:
        joinedFile = open('ids.txt', 'a')
        joinedFile.write(str(message.chat.id) + '\n')
        joinedUsers.add(message.chat.id)

    user_id = [message.from_user.first_name, message.from_user.last_name, message.from_user.username]            #Заполнение списка всех пользователей бота
    if user_id not in users:
        users.append(user_id)
        global c_users
        c_users += 1

    bot.send_message(message.chat.id, f'Приветсвую, {message.from_user.first_name}')
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Расписание')   #имена для кнопок
    btn2 = types.KeyboardButton('Помощь')        #имена для кнопок
    btn3 = types.KeyboardButton('Перезапустить')  #имена для кнопок
    markup.row(btn1)     #Создаёт кнопку под вводом 1 ряд
    markup.row(btn2)     #Создаёт кнопку под вводом 2 ряд
    markup.row(btn3)     #Создаёт кнопку под вводом 3 ряд
    bot.send_message(message.chat.id, f'Список команд для этого бота:\n/start - перезапустить\n/help - список команд\n/rasp - Расписание', reply_markup=markup)



@bot.message_handler(commands=['help'])        #при вводе команды help вылезает сообщение
def info(message):
    bot.send_message(message.chat.id,f'Список команд для этого бота:\n/start - перезапустить\n/help - список команд\n/rasp - Расписание')


@bot.message_handler(commands=['rasp'])        #при вводе команды rasp вылезает сообщение
def rasp(message):
    markup_inline = types.InlineKeyboardMarkup()
    kbtn42 = types.InlineKeyboardButton('5 класс', callback_data='5')      #даём имя кнопке, присваиваем ей класс и коллбэк дату
    kbtn43 = types.InlineKeyboardButton('6 класс', callback_data='6')
    kbtn44 = types.InlineKeyboardButton('7 класс', callback_data='7')
    kbtn45 = types.InlineKeyboardButton('8 класс', callback_data='8')
    kbtn46 = types.InlineKeyboardButton('9 класс', callback_data='9')
    kbtn47 = types.InlineKeyboardButton('10 класс', callback_data='10')
    kbtn48 = types.InlineKeyboardButton('11 класс', callback_data='11')
    markup_inline.row(kbtn42, kbtn43)             #собсна выводим то шо сделали
    markup_inline.row(kbtn44, kbtn45)
    markup_inline.row(kbtn46)
    markup_inline.row(kbtn47)
    markup_inline.row(kbtn48)
    bot.send_message(message.chat.id, 'Выберите класс:', reply_markup= markup_inline)

@bot.message_handler(func=lambda message: True)         #постоянная работа функции
def on_click(message):            #по сути дублирование всех команд но для работы нужна кнопка
    if message.text == 'Расписание':
        markup_inline = types.InlineKeyboardMarkup()
        kbtn42 = types.InlineKeyboardButton('5 класс', callback_data='5')        #имя,тип,текст и кол бэк дата
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
        bot.send_message(message.chat.id, 'Выберите класс:', reply_markup = markup_inline)     #воводятся с этим текстом

    elif message.text == 'Помощь':
        bot.send_message(message.chat.id, f'Список команд для этого бота:\n/start - перезапустить\n/help - список команд\n/rasp - Расписание')

    elif message.text == 'Разработчик':
        bot.send_message(message.chat.id, 'Это Гриша сделал(и немного вова)')

    elif message.text == 'Перезапустить':
        if not str(message.chat.id) in joinedUsers:
            joinedFile = open('ids.txt', 'a')
            joinedFile.write(str(message.chat.id) + '\n')
            joinedUsers.add(message.chat.id)

        user_id = [message.from_user.first_name, message.from_user.last_name,
                   message.from_user.username]  # Заполнение списка всех пользователей бота
        if user_id not in users:
            users.append(user_id)
            global c_users
            c_users += 1

        bot.send_message(message.chat.id, f'Приветсвую, {message.from_user.first_name}')
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Расписание')  # имена для кнопок
        btn2 = types.KeyboardButton('Помощь')  # имена для кнопок
        btn3 = types.KeyboardButton('Перезапустить')  # имена для кнопок
        markup.row(btn1)  # Создаёт кнопку под вводом 1 ряд
        markup.row(btn2)  # Создаёт кнопку под вводом 2 ряд
        markup.row(btn3)  # Создаёт кнопку под вводом 3 ряд
        bot.send_message(message.chat.id, f'Список команд для этого бота:\n/start - перезапустить\n/help - список команд\n/rasp - Расписание', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)     #про это я писал
def clasrasp(call): #тут идёт обращение к калу
    global selectGroup
    markup_inline = types.InlineKeyboardMarkup()
    dbtn1 = types.InlineKeyboardButton('Сегодня', callback_data='Сегодня')
    dbtn2 = types.InlineKeyboardButton('Завтра', callback_data='Завтра')
    if call.data == '5':       # если это пришло то выполняется действия ниже и тд
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
            url = 'https://rasp.milytin.ru/search'
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

            for item in data[0]:
                for lesson in item:
                    bot.send_message(call.message.chat.id, lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["teacher"] + ' | ' + lesson["place"])
        except IndexError:
            bot.send_message(call.message.chat.id, 'Расписание ещё не выложили!')

    elif call.data == 'Завтра':
        try:
            selectDate = datetime.datetime.now()
            selectDate = selectDate + datetime.timedelta(days=1)
            selectDate = selectDate.strftime('%Y-%m-%d')
            selectDate = f'{selectDate}'
            url = 'https://rasp.milytin.ru/search'
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

            for item in data[0]:
                for lesson in item:
                    bot.send_message(call.message.chat.id, lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["teacher"] + ' | ' + lesson["place"])
        except IndexError:
            bot.send_message(call.message.chat.id, 'Расписание ещё не выложили!')

bot.polling(none_stop=True)