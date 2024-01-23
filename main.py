import telebot
from telebot import types
import webbrowser
import sqlite3
import openpyxl

bot = telebot.TeleBot('6741433926:AAFAOv4jNejzzQD_Gs7KxLtXA-xluG8jAcU')

users = []
c_users = 0
rasp = openpyxl.open('rasp.xlsx', read_only=True)
sheet1 = rasp.active
raspy = openpyxl.open('raspy.xlsx', read_only=True)
sheet12 = rasp.active


#доделать
@bot.message_handler(commands=['post6741433926'])
def post(message):
    bot.send_message(message.chat.id, f'Отправьте файл с расписанием для ученика')
#доделать

@bot.message_handler(commands=['mg'])    #команда только для разработчиков, нужна для просмотра информации о чате и пользователе
def mg(message):
    bot.send_message(message.chat.id, message)
    bot.send_message(message.chat.id, f'Все пользователи:')
    for item in users:
        bot.send_message(message.chat.id, f'{item}')

    bot.send_message(message.chat.id, f'Всего пользователей: {c_users}')

@bot.message_handler(commands=['start'])  #Команда для запуска бота и его стартовой функции
def start(message):
    user_id = [message.from_user.first_name, message.from_user.last_name, message.from_user.username]            #Заполнение списка всех пользователей бота
    if user_id not in users:
        users.append(user_id)
        global c_users
        c_users += 1

    bot.send_message(message.chat.id, f'Приветсвую, {message.from_user.first_name}')
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Расписание для учеников')   #имена для кнопок
    btn2 = types.KeyboardButton('Помощь')        #имена для кнопок
    btn3 = types.KeyboardButton('Расписание для учителей')    #имена для кнопок
    btn4 = types.KeyboardButton('Перезапустить')  #имена для кнопок
    markup.row(btn1, btn3)     #Создаёт кнопку под вводом 1 ряд
    markup.row(btn2)     #Создаёт кнопку под вводом 2 ряд
    markup.row(btn4)     #Создаёт кнопку под вводом 3 ряд
    bot.send_message(message.chat.id, f'Список команд для этого бота:', reply_markup=markup)
    bot.send_message(message.chat.id, '/start - перезапустить')
    bot.send_message(message.chat.id, '/help - список команд')
    bot.send_message(message.chat.id, '/rasp - Расписание для учеников')
    bot.send_message(message.chat.id, '/raspy - расписание для учителей')



@bot.message_handler(commands=['help'])
def info(message):
    bot.send_message(message.chat.id, f'Список команд для этого бота:')
    bot.send_message(message.chat.id, '/start - перезапустить')
    bot.send_message(message.chat.id, '/help - список команд')
    bot.send_message(message.chat.id, '/rasp - Расписание для учеников')
    bot.send_message(message.chat.id, '/raspy - расписание для учителей')

@bot.message_handler(commands=['rasp'])
def rasp(message):
    bot.send_message(message.chat.id, 'Расписание для учеников')
    rasp = open('./rasp.xlsx', 'rb')
    bot.send_document(message.chat.id, rasp)

@bot.message_handler(commands=['raspy'])
def raspy(message):
    bot.send_message(message.chat.id, 'Расписание для учителей')
    raspy = open('./raspy.xlsx', 'rb')
    bot.send_document(message.chat.id, raspy)

@bot.message_handler(func=lambda message: True)
def on_click(message):
    if message.text == 'Расписание для учеников':
        bot.send_message(message.chat.id, 'Расписание для учеников')
        rasp = open('./rasp.xlsx', 'rb')
        bot.send_document(message.chat.id, rasp)
    elif message.text == 'Расписание для учителей':
        bot.send_message(message.chat.id, 'Расписание для учителей')
        raspy = open('./raspy.xlsx', 'rb')
        bot.send_document(message.chat.id, raspy)
    elif message.text == 'Помощь':
        bot.send_message(message.chat.id, f'Список команд для этого бота:')
        bot.send_message(message.chat.id, '/start - перезапустить')
        bot.send_message(message.chat.id, '/help - список команд')
        bot.send_message(message.chat.id, '/rasp - Расписание для учеников')
        bot.send_message(message.chat.id, '/raspy - расписание для учителей')
    elif message.text == 'Разработчик':
        bot.send_message(message.chat.id, 'Это Гриша сделал')
    elif message.text == 'Перезапустить':
        user_id = [message.from_user.first_name, message.from_user.last_name,
        message.from_user.username]  # Заполнение списка всех пользователей бота
        if user_id not in users:
            users.append(user_id)
            global c_users
            c_users += 1

        bot.send_message(message.chat.id, f'Приветсвую, {message.from_user.first_name}')
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Расписание для учеников')  # имена для кнопок
        btn2 = types.KeyboardButton('Помощь')  # имена для кнопок
        btn3 = types.KeyboardButton('Расписание для учителей')  # имена для кнопок
        btn4 = types.KeyboardButton('Перезапустить')  # имена для кнопок
        markup.row(btn1, btn3)  # Создаёт кнопку под вводом 1 ряд
        markup.row(btn2)  # Создаёт кнопку под вводом 2 ряд
        markup.row(btn4)  # Создаёт кнопку под вводом 3 ряд
        bot.send_message(message.chat.id, f'Список команд для этого бота:', reply_markup=markup)
        bot.send_message(message.chat.id, '/start - перезапустить')
        bot.send_message(message.chat.id, '/help - список команд')
        bot.send_message(message.chat.id, '/rasp - Расписание для учеников')
        bot.send_message(message.chat.id, '/raspy - расписание для учителей')


bot.polling(none_stop=True)