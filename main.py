import threading
import telebot
from telebot import types
import requests
import json
import datetime
import sqlite3
from telebot import apihelper
import time
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import fitz
from PIL import Image
import shutil


apihelper.proxy = {'HTTP': 'httph://217.13.102.86:3128'}

runCheck = True

global page
page = 1

global classesAll
classesAll = [
    '5а', '5б', '5в', '5г', '5д', '5е', '5ж', '5з', '5и', '5к', '5л', '5м', '5н',
    '6а', '6г', '6д', '6е', '6ж', '6з', '6б', '6в', '6и', '6к', '6л', '6м', '6н',
    '7а', '7б', '7в', '7г', '7д', '7е', '7ж', '7з', '7и',
    '8а', '8б', '8в', '8г', '8д', '8е', '8к', '8ж', '8з', '8и',
    '9а', '9б', '9в', '9г', '9д', '9е', '9ж', '9з', '9и', '9к',
    '10а', '10б', '10в', '10г',
    '11а', '11б', '11в'
]

global classesAllIds
classesAllIds = [
    '212', '213', '214', '215', '216', '217', '218', '219', '220', '268', '269', '270', '271',
    '221', '224', '225', '226', '227', '228', '258', '259', '272', '442', '443', '444', '445',
    '229', '230', '231', '232', '233', '260', '273', '274', '446',
    '235', '236', '237', '238', '239', '240', '244', '261', '262', '263',
    '245', '246', '247', '248', '249', '250', '264', '265', '266', '267',
    '251', '252', '253', '447',
    '254', '255', '256'
]

global teachersAll
teachersAll = [
    "Тучанская В.В.", "Андриевская Н.И.", "Логинова О.П.", "Борзенина М.А.", "Цыб Т.В.",
    "Морозова Ю.А.", "Петренко Н.С.", "Коротких А.И.", "Пилостаева А.О.", "Некрасова Н.В.",
    "Семушина И.Л.", "Тараторина О.В.", "Шилова В.А.", "Стрелкова М.А.", "Кубык К.Р.",
    "Попова М.С.", "Синева Т.А.", "Санникова Е.А.", "Кашина А.Ю.", "Корнилова В.В.",
    "Абрамова Н.С.", "Илларионова В.П.", "Коргинова А.В.", "Павлова Я.М.", "Горбунова М.А.",
    "Ларчина Т.В.", "Соколова Е.Е.", "Семочкина А.А.", "Ципилева Т.А.", "Шевченко А.А.",
    "Фёдорова К.Р.", "Бесова Л.А.", "Бокарева А.А.", "Горбатович А.А.", "Рябкова С.Н.",
    "Джанасова Н.Н.", "Кистанова Н.Л.", "Крылова Т.В.", "Пелевина Н.В.", "Гаджиева М.Г.",
    "Яичкова М.М.", "Каронова С.Г.", "Филиппова Т.В.", "Савинова К.В.", "Комарова Л.А.",
    "Бурмистрова О.Ю.", "Крутикова Я.В.", "Мокина И.Р.", "Царева М.А.", "Савина И.В.",
    "Кузнецова М.А.", "Самсонова Т.М.", "Костина М.В.", "Хонина Е.А.", "Панина Е.В.",
    "Петровичева А.А.", "Божко А.А.", "Балакшин Р.Н.", "Мащенка П.А.", "Богданова Е.В.",
    "Ананьина И.К.", "Григорьева Д.А.", "Алексеева Т.В.", "Груздева И.Н.", "Проскурина Е.Н.",
    "Постникова О.В.", "Гаврилова Н.Н.", "Смирнова Е.А.", "Ильиных И.В.", "Новичихина Т.С.",
    "Патютько Е.А.", "Гордеев М.А.", "Коршунова Р.С.", "Харчева Е.Н.", "Соболева И.С.",
    "Соболева Е.А.", "Чистякова Ю.О.", "Лебедева Т.В.", "Флегантова Н.С.", "Лясникова Н.Д.",
    "Корзина Ю.В.", "Караваева В.А.", "Ананьина О.Н.", "Горинова Д.В.", "Васильев И.Н.",
    "Щерба Е.Ю.", "Першичева Е.В.", "Петрова В.О.", "Агеева Л.Г.", "Матвева Е.А.",
    "Туницкая О.Ю.", "Гаврилова О.В.", "Репкина А.В.", "Елисеева О.Г.", "Савинова О.В.",
    "Заборихина Ю.Л.", "Ярулина В.Р.", "Васильева С.Н.", "Мащенко П.А.", "Соболева А.Н.",
    "Куражова Н.Ю.", "Галова А.В.", "Синицына А.Н.", "Федорова Л.В.", "Манаев И.А.",
    "Матвеева Е.А.", "Громова Т.В.", "Юсуфович С.А.", "Смирнова В.А.", "Лисоцкова О.Н.",
    "Борзунова Ю.А.", "Ситников П.Л.", "Трифанова М.С.", "Горушкина А.В.", "Калиняк Л.В.",
    "Иванова С.Г.", "Коробов А.В.", "Байрамова Л.С.", "Ефипова М.П.", "Кронштатова Е.А.",
    "Синицина А.Н.", "Табунов И.А.", "Глухова О.А.", "Горинава Д.В.", "Кириллов А.А.",
    "Качкина А.Н.", "Фёдоров М.Д.", "Неклюдова Е.А.", "Кукушкина А.А.", "Фёдорова М.Д.",
    "Белякова О.С.", "Семушина И.А.", "Смирнов А.А.", "Разлетова В.В.", "Стеценко Н.Д.",
    "Калиняк Л.Г.", "Завьялова А.Н.", "Феофанова Е.А.", "Горелова А.В.", "Мелкова Е.Ю.",
    "Кушева Т.А.", "Елмалджиди Е.Г.", "Крыскина К.А.", "Истоцкая Н.Н.", "Николаева Т.В.",
    "Нестерова В.И.", "Кочуева А.С.", "Мартынов П.С.", "Щукина О.И.", "Калёва В.В.",
    "Череповецкий Н.З.", "Коковкина Е.С.", "Востокова А.С.", "Ситникова Я.В.", "Шведова А.А.",
    "Андреева А.С.", "Кумбула М.С.", "Агапова М.М.", "Булычева А.А.", "Куракина О.Г.",
    "Коптяева О.А.", "Короглуева А.И.", "Кузнецова Е.И.", "Петяева А.В.", "Угрюмова В.И.",
    "Мартынив А.И.", "Черняева С.Е.", "Кривоборская В.А.", "Корзникова Ю.С.", "Лебедева Ю.А.",
    "Елмаджиди Е.Г.", "Курникова П.В.", "Федорова К.Р.", "Овчинникова Т.В.", "Фомина Ю.И.",
    "Коркина Н.А.", "Калева В.В.", "Хребтова А.Р.", "Мащенко М.П.", "Иванова Е.А.",
    "Мухина Л.Н.", "Соколова И.В.", "Сулейманова А.В.", "Сулейманова В.А.", "Харчева Е.А.",
    "Шешуев Г.А.", "Базовая И.Ю.", "Торочкова А.А.", "Ключникова К.А.", "Сергеева А.Д.",
    "Малинина Д.А.", "Мокина А.М.", "Мокина А.В.", "Твердохлеб К.К.", "Мурашкина С.В.",
    "Смирнова К.В.", "Ситников П.С.", "Шалаева С.А.", "Мышенкова Е.М.", "Грошевихин А.Н.",
    "Маурашкина С.В.", "Мурашкина С.А.", "Недайводина П.И.", "Сошникова А.В.", "Колотыгина А.А.",
    "Павлова О.В.", "Белова И.И.", "Карышева Е.А.", "Шандакова И.Л.", "Галстукова Е.И.",
    "Маврова В.Е.", "Гаевская И.К.", "Черепанова М.Н.", "Очеленкова Т.В.", "Печкарева В.В.",
    "Муращкина С.В.", "Егорова Е.А.", "Лазарева А.А.", "Печарева В.В."
]

global teachersAllIds
teachersAllIds = [
    "222", "223", "224", "225", "226", "227", "228", "229", "230", "231", "232", "233", "234", "235", "236",
    "237", "238", "239", "240", "241", "242", "244", "246", "247", "248", "249", "250", "251", "252", "253",
    "254", "255", "256", "257", "259", "260", "261", "262", "263", "264", "265", "266", "267", "268", "269",
    "270", "271", "272", "273", "274", "275", "276", "277", "278", "279", "280", "281", "282", "283", "284",
    "285", "286", "287", "288", "289", "290", "291", "293", "294", "295", "296", "297", "298", "299", "300",
    "301", "302", "303", "304", "305", "306", "307", "308", "309", "310", "311", "312", "313", "314", "315",
    "316", "317", "318", "319", "320", "321", "322", "323", "324", "326", "327", "329", "330", "331", "332",
    "333", "334", "335", "336", "337", "338", "339", "340", "341", "344", "346", "348", "351", "359", "360",
    "384", "393", "394", "396", "399", "400", "401", "402", "403", "405", "408", "409", "412", "416", "468",
    "470", "477", "504", "514", "515", "517", "518", "519", "520", "522", "523", "524", "525", "526", "527",
    "528", "529", "530", "531", "532", "534", "535", "537", "538", "539", "540", "541", "542", "543", "544",
    "545", "547", "548", "551", "553", "554", "555", "556", "557", "560", "574", "589", "590", "607", "621",
    "622", "623", "627", "628", "631", "644", "645", "646", "647", "648", "651", "652", "655", "660", "664",
    "667", "669", "679", "680", "681", "683", "687", "697", "711", "712", "713", "714", "715", "717", "718",
    "719", "723", "727", "728", "733", "734", "739", "741", "752"
]

global url
url = 'https://rasp.milytin.ru/search'

bot = telebot.TeleBot('7889392387:AAF1L7JF39KpR0xpu7JR-lx2Ft7KSQjLv4I')


def mainRaspUpdate():
    while True:
        print(f"{time.ctime(time.time())}:Запускаю проверку!!")
        if checkRaspUpdate():
            print(f"{time.ctime(time.time())}:Рассылка начата!")
            sendRaspUpdate()
            print(f"{time.ctime(time.time())}:Рассылка закончена!")
            time.sleep(14 * 60 * 60)
        else:
            print(f"{time.ctime(time.time())}:Таймер на 10 минут запущен!")
            time.sleep(10 * 60)


def checkRaspUpdate():
    params = {
        'selectGroup': '248',
        'selectTeacher': '222',
        'selectPlace': '174',
        'selectDate[]': f"{(datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')}",
        'type': 'group'
    }
    response = requests.get(url, params=params)
    response = response.json()
    response = json.loads(response)
    print(time.ctime(time.time()), response)
    if response != []:
        return True

    return False


def sendRaspUpdate():
    shutil.copy("ids.db", "ids2.db")
    conn = sqlite3.connect('ids2.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    selectDate = datetime.datetime.now() + datetime.timedelta(days=1)
    selectDate = f"{selectDate.strftime('%Y-%m-%d')}"
    for user in users:
        infu = user[0]
        cur.execute(f"SELECT autoSchedule FROM users WHERE id = {infu}")
        autoSchedule = str(cur.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
        if autoSchedule == None:
            cur.execute('UPDATE users SET autoSchedule = ? WHERE id = ?', (1, infu))
        elif autoSchedule == '0':
            continue

        try:
            cur.execute(f"SELECT class_name_temp FROM users WHERE id = {infu}")
            cur.execute("SELECT class_id FROM classes WHERE class_name = (SELECT class_name FROM users WHERE id = ?)", (infu,))
            selectGroup = str(cur.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
            cur.execute(f'''SELECT schedule_form FROM users WHERE id = {infu}''')
            schedule_form = str(cur.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
            cur.execute(f'''SELECT teacher_exist FROM users WHERE id = {infu}''')
            teacher_exist = str(cur.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
            if teacher_exist == 'None':
                cur.execute('UPDATE users SET teacher_exist = ? WHERE id = ?', ('1', infu))
                teacher_exist = '1'

            if schedule_form == 'None':
                cur.execute('UPDATE users SET schedule_form = ? WHERE id = ?', ('1', infu))
                schedule_form = '1'
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
            if data == []:
                continue

            if schedule_form == '1':
                message = []
                for item in data[0]:
                    for lesson in item:
                        if teacher_exist == '1':
                            message.append(lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["teacher"] + ' | ' + lesson["place"])
                        elif teacher_exist == '0':
                            message.append(lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["place"])
                createImage(message, infu, teacher_exist)
                with open(f'img/table{infu}.jpg', 'rb') as photo:
                    bot.send_photo(infu, photo, selectDate)
            else:
                message = ''
                for item in data[0]:
                    for lesson in item:
                        if teacher_exist == '1':
                            message += lesson["time"] + '\n' + lesson["discipline"] + ' | ' + lesson["teacher"] + ' | ' + lesson["place"] + '\n' + '-' + '\n'
                        elif teacher_exist == '0':
                            message += lesson["time"] + '\n' + lesson["discipline"] + ' | ' + lesson["place"] + '\n' + '-' + '\n'
                bot.send_message(infu, f'Расписание на {selectDate}\n{message}')
        except Exception as e:
            print(f"{infu}, {str(e)}")
            continue

    cur.close()
    conn.close()


raspCheck_thread = threading.Thread(target=mainRaspUpdate)
raspCheck_thread.daemon = True
raspCheck_thread.start()

@bot.message_handler(commands=['postToAll23'])
def post(message):
    bot.delete_message(message.chat.id, message.message_id)
    user_id = message.from_user.id
    if user_id == 6042204485 or user_id == 1374973615 or user_id == 5818281440:
        shutil.copy('ids.db', 'ids2.db')
        conn = sqlite3.connect('ids2.db')
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
    else:
        bot.send_message(message.chat.id, 'Нинада')


@bot.message_handler(commands=['mg'])
def mg(message):
    bot.delete_message(message.chat.id, message.message_id)
    user_id = message.from_user.id
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur.execute('SELECT * FROM classes')
    classes = cur.fetchall()
    cur.execute('SELECT * FROM teachers')
    teachers = cur.fetchall()
    cur.close()
    conn.close()
    if user_id == 6042204485 or user_id == 1374973615 or user_id == 5818281440:
        inf = 0
        for user in users:
            inf += 1

        classesinf = ''
        for classesi in classes:
            print(classesi)

        for teacher in teachers:
            print(teacher)

        bot.send_message(message.chat.id, f'Количество пользователей: {inf}')
        bot.send_document(message.chat.id, open(r'mainEx.py', 'rb'))
        bot.send_document(message.chat.id, open(r'ids.db', 'rb'))
    else:
        bot.send_message(message.chat.id, f'Ты откуда это узнал?')


@bot.message_handler(commands=['start'])
def start(message):
    bot.delete_message(message.chat.id, message.message_id)
    user_id = message.from_user.id
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, class_name TEXT, class_name_temp TEXT, page TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS classes (class_name TEXT, class_id TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS teachers (teacher_name TEXT, teacher_id TEXT)''')
    cur.execute(f"PRAGMA table_info(users)")
    columns = cur.fetchall()
    table_exist = False
    if not any(name[1] == 'teacher_exist' for name in columns):
        cur.execute('''ALTER TABLE users ADD COLUMN teacher_exist INTEGER''')

    if not any(column[1] == 'schedule_form' for column in columns):
        cur.execute('''ALTER TABLE users ADD COLUMN schedule_form INTEGER''')

    if not any(column[1] == 'autoSchedule' for column in columns):
        cur.execute('''ALTER TABLE users ADD COLUMN autoSchedule INTEGER''')

    conn.commit()
    cur.execute('''SELECT class_name FROM classes''')
    firstSlot = cur.fetchone()
    if firstSlot is not None:
        pass
    else:
        for className, classId in zip(classesAll, classesAllIds):
            cur.execute('''INSERT INTO classes (class_name, class_id) VALUES (?, ?)''', (className, classId))
        for teacherName, teacherId in zip(teachersAll, teachersAllIds):
            cur.execute('''INSERT INTO teachers (teacher_name, teacher_id) VALUES (?, ?)''', (teacherName, teacherId))
    conn.commit()
    cur.execute('''SELECT id FROM users''')
    secondSlot = cur.fetchall()
    if (user_id,) not in secondSlot:
        cur.execute('''INSERT INTO users (id, page, schedule_form, teacher_exist, autoSchedule) VALUES (?, ?, ?, ?, ?)''', (user_id, 1, 1, 1, 1))
    conn.commit()
    cur.close()
    conn.close()
    if user_id == 6042204485 or user_id == 1374973615 or user_id == 5818281440:
        bot.send_message(message.chat.id, f'Слався о великий создатель {message.from_user.first_name}')
    elif user_id == 1623556809 or user_id == 1544399322:
        bot.send_message(message.chat.id, f'Слався о великая {message.from_user.first_name}')
    else:
        bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name}')
    changeClas(message)


def user_clas(message, clas, id):
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    cur.execute('SELECT id FROM users')
    userId = cur.fetchall()
    if id not in [x[0] for x in userId]:
        cur.execute('INSERT INTO users (id, class_name, page, schedule_form, teacher_exist, autoSchedule) VALUES (?, ?, ?, ?, ?, ?)', (id, clas, 1, 1, 1, 1))
    else:
        cur.execute("UPDATE users SET class_name = ? WHERE id = ?", (clas, id))
        cur.execute("UPDATE users SET page = ? WHERE id = ?", (1, id))
    conn.commit()
    cur.close()
    conn.close()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Расписание')
    btn2 = types.KeyboardButton('Помощь')
    btn3 = types.KeyboardButton('Перезапустить')
    btn4 = types.KeyboardButton('Поменять класс')
    btn5 = types.KeyboardButton('Настройки')
    btn6 = types.KeyboardButton('Сегодня')
    btn7 = types.KeyboardButton('Завтра')
    markup.row(btn6, btn1, btn7)
    markup.row(btn2, btn5, btn4)
    markup.row(btn3)
    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
    bot.send_message(message.chat.id, text = f'Список команд для этого бота:\n/start - перезапустить\n/help - список команд\n/rasp - Расписание\n/changeClas - поменять класс\n/settings - настройки\nВаш класс: {clas}', reply_markup=markup)


@bot.message_handler(commands=['help'])
def info(message):
    bot.delete_message(message.chat.id, message.message_id)
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
        changeClas(message)
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
    bot.send_message(chat_id = message.chat.id, text = f'Ваш класс: {clas}\nСписок команд для этого бота:\n/start - перезапустить\n/help - список команд\n/settings - поменять класс\n/rasp - Расписание\n/thelp - Попросить помощи\nПример: /thelp помогите, мой класс не отображается!')


@bot.message_handler(commands=['settings'])
def settings(message):
    bot.delete_message(message.chat.id, message.message_id)
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    usid = message.from_user.id
    cur.execute(f'SELECT class_name FROM users WHERE id = {usid}')
    rows = cur.fetchall()
    clas = f'{rows}'
    clas = clas.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "").replace("'", "").replace(",", "")
    cur.execute(f'SELECT teacher_exist FROM users WHERE id = {usid}')
    teacher_exist = cur.fetchall()[0][0]
    if teacher_exist == 0:
        teacher_exist = '🔴'
    else:
        teacher_exist = '🟢'
    cur.execute(f'SELECT autoSchedule FROM users WHERE id = {usid}')
    autoShedule = cur.fetchall()[0][0]
    if autoShedule == 0:
        autoShedule = '🔴'
    else:
        autoShedule = '🟢'
    cur.close()
    conn.close()
    if clas == '':
        changeClas(message)
        return
    m = types.InlineKeyboardMarkup()
    changeScheduleFormBut = types.InlineKeyboardButton('Дизайн расписания', callback_data='changeScheduleForm')
    changeTeacherExistBut = types.InlineKeyboardButton(f'{teacher_exist}учителя в расписании', callback_data='changeTeacherExist')
    changeAutoScheduleBut = types.InlineKeyboardButton(f'{autoShedule}Авто-расписание', callback_data='changeAutoSchedule')
    m.row(changeScheduleFormBut)
    m.row(changeTeacherExistBut)
    m.row(changeAutoScheduleBut)
    bot.send_message(message.chat.id, 'Возможные опции:', reply_markup=m)



@bot.message_handler(commands=['thelp'])
def tHelp(message):
    mes = message.text[message.text.find(' '):]
    mes = mes[1:]
    ids = [6042204485, 1374973615]
    requaier = message.from_user.username
    requaiers_name = str(message.from_user.first_name) + ' ' + str(message.from_user.last_name)
    if mes != '':
        for tex in ids:
            try:
                bot.send_message(tex, f'Жалоба от @{requaier}\nОн же {requaiers_name}:\n{mes}')
            except:
                pass
        bot.send_message(message.chat.id, 'Ваша жалоба отправлена!')
    else:
        bot.send_message(message.chat.id, 'Жалоба долна включать в себя сообщение!\nПример: /thelp мой класс не отображается')


@bot.message_handler(commands=['rasp'])
def rasp(message):
    bot.delete_message(message.chat.id, message.message_id)
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    usid = message.from_user.id
    cur.execute(f'SELECT class_name FROM users WHERE id = {usid}')
    rows = cur.fetchall()
    cur.execute('''UPDATE users SET page = 1''')
    conn.commit()
    clas = f'{rows}'
    clas = clas.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "").replace("'", "").replace(",", "")
    cur.close()
    conn.close()
    if clas == '':
        changeClas(message)
        return
    markup_inline = types.InlineKeyboardMarkup()
    if clas[0] != '1' and clas[0] != '0' and clas[0] != '5' and clas[0] != '6' and clas[0] != '7' and clas[0] != '8' and clas[0] != '9':
        bbtn1 = types.InlineKeyboardButton(f'{clas}', callback_data=f'{clas}' + 'G')
    else:
        bbtn1 = types.InlineKeyboardButton(f'{clas}', callback_data=f'{clas}' + 'V')
    bbtn2 = types.InlineKeyboardButton('Все классы', callback_data='All')
    bbtn3 = types.InlineKeyboardButton('Учителя', callback_data='Teach')
    markup_inline.row(bbtn1, bbtn2)
    markup_inline.row(bbtn3)
    bot.send_message(message.chat.id, text = 'Что вы хотите посмотреть?', reply_markup=markup_inline)


@bot.message_handler(commands=['changeClas'])
def changeClas(message):
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
    Kbtn1 = types.InlineKeyboardButton('5 класс', callback_data='5P')
    Kbtn2 = types.InlineKeyboardButton('6 класс', callback_data='6P')
    Kbtn3 = types.InlineKeyboardButton('7 класс', callback_data='7P')
    Kbtn4 = types.InlineKeyboardButton('8 класс', callback_data='8P')
    Kbtn5 = types.InlineKeyboardButton('9 класс', callback_data='9P')
    Kbtn6 = types.InlineKeyboardButton('10 класс', callback_data='10P')
    Kbtn7 = types.InlineKeyboardButton('11 класс', callback_data='11P')
    Kbtn8 = types.InlineKeyboardButton('Учитель', callback_data='TeachH')
    markup_inline.row(Kbtn1, Kbtn2)
    markup_inline.row(Kbtn3, Kbtn4)
    markup_inline.row(Kbtn5)
    markup_inline.row(Kbtn6)
    markup_inline.row(Kbtn7)
    markup_inline.row(Kbtn8)
    bot.send_message(message.chat.id, 'Укажите ваш класс:', reply_markup=markup_inline)


def send_rasp2(message, selectDate):
    try:
        infu = message.from_user.id
        selectDate = selectDate.strftime('%Y-%m-%d')
        shutil.copy("ids.db", "ids2.db")
        conn = sqlite3.connect('ids2.db')
        cur = conn.cursor()
        cur.execute("SELECT class_id FROM classes WHERE class_name = (SELECT class_name FROM users WHERE id = ?)", (infu,))
        selectGroup = str(cur.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
        cur.execute(f'''SELECT schedule_form FROM users WHERE id = {infu}''')
        schedule_form = str(cur.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
        cur.execute(f'''SELECT teacher_exist FROM users WHERE id = {infu}''')
        teacher_exist = str(cur.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
        if teacher_exist == 'None':
            cur.execute('UPDATE users SET teacher_exist = ? WHERE id = ?', ('1', infu))
            teacher_exist = '1'

        if schedule_form == 'None':
            cur.execute('UPDATE users SET schedule_form = ? WHERE id = ?', ('1', infu))
            schedule_form = '1'
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
        if schedule_form == '1':
            message = []
            for item in data[0]:
                for lesson in item:
                    if teacher_exist == '1':
                        message.append(lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["teacher"] + ' | ' + lesson["place"])
                    elif teacher_exist == '0':
                        message.append(lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["place"])
            createImage(message, infu, teacher_exist)
            with open(f'img/table{infu}.jpg', 'rb') as photo:
                bot.send_photo(infu, photo, selectDate)
        else:
            message = ''
            for item in data[0]:
                for lesson in item:
                    if teacher_exist == '1':
                        message += lesson["time"] + '\n' + lesson["discipline"] + ' | ' + lesson["teacher"] + ' | ' + lesson["place"] + '\n' + '-' + '\n'
                    elif teacher_exist == '0':
                        message += lesson["time"] + '\n' + lesson["discipline"] + ' | ' + lesson["place"] + '\n' + '-' + '\n'
            bot.send_message(infu, f'Расписание на {selectDate}\n{message}')

        cur.close()
        conn.close()

    except IndexError:
        bot.send_message(infu, "Расписание ещё не выложили!")



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

    elif message.text == 'Поменять класс':
        bot.delete_message(message.chat.id, message.message_id)
        changeClas(message)

    elif message.text == 'Сегодня':
        send_rasp2(message, datetime.datetime.now())

    elif message.text == 'Завтра':
        selectDate = datetime.datetime.now()
        selectDate = selectDate + datetime.timedelta(days=1)
        send_rasp2(message, selectDate)

    elif message.text.lower() == 'разработчик':
        bot.send_message(message.chat.id, 'Сие творение создал Григорий и моральную помощь оказывал его юный подаван Владимир\nГригорий: @FIVE_HH, 89110483340(кому не сложно скиньте денег)\nВладимир: @Discketaa, 89216874164\nЕсли вы увидели это сообщение, то обязаны нам написать или позвонить!')

    elif message.text.lower() == 'владимир путин':
        bot.send_message(message.chat.id, 'Молодец!\nПолитик, лидер и боец!')



def createImage(message, id, teacher_exist):
    pdfmetrics.registerFont(TTFont('CustomFont', 'img/font.ttf'))
    if teacher_exist == '1':
        data = [
            ["Время", "Урок", "Учитель", "Класс"],
        ]
    elif teacher_exist == '0':
        data = [
            ["Время", "Урок", "Класс"],
        ]

    for line in message:
        data.append(line.split(' | '))

    pdf = SimpleDocTemplate(f"img/table{id}.pdf", pagesize=letter)
    elements = []
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'CustomFont'),
        ('FONTNAME', (0, 1), (-1, -1), 'CustomFont'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    pdf.build(elements)

    pdf_document = fitz.open(f"img/table{id}.pdf")
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        pix.save(f"img/table{id}.jpg")

        img = Image.open(f"img/table{id}.jpg")
        img = img.convert("RGBA")
        data = img.getdata()
        min_x = img.width
        min_y = img.height
        max_x = 0
        max_y = 0

        for y in range(img.height):
            for x in range(img.width):
                r, g, b, a = data[y * img.width + x]
                if (r, g, b) != (255, 255, 255):
                    if x < min_x:
                        min_x = x
                    if x > max_x:
                        max_x = x
                    if y < min_y:
                        min_y = y
                    if y > max_y:
                        max_y = y

        cropped_img = img.crop((min_x + 1, min_y + 7, max_x - 5, max_y))
        cropped_img = cropped_img.convert("RGB")
        cropped_img.save(f"img/table{id}.jpg")

    pdf_document.close()


@bot.callback_query_handler(func=lambda call: True)
def clasrasp(call):
    global user_id
    global page
    user_id = call.from_user.id
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    dbtn1 = types.InlineKeyboardButton('Сегодня', callback_data='Сегодня')
    dbtn2 = types.InlineKeyboardButton('Завтра', callback_data='Завтра')
    dbtn3 = types.InlineKeyboardButton('Сегодня', callback_data='СегодняTE')
    dbtn4 = types.InlineKeyboardButton('Завтра', callback_data='ЗавтраTE')


    def next_message_rasp(clas):
        markup_inline.row(dbtn1, dbtn2)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Выберите дату', reply_markup=markup_inline)

    def next_message_rasp_teach(clas):
        conn = sqlite3.connect('ids.db')
        cur = conn.cursor()
        cur.execute('''UPDATE users SET page = 1''')
        conn.commit()
        cur.close()
        conn.close()
        markup_inline.row(dbtn3, dbtn4)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Выберите дату', reply_markup=markup_inline)

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
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Выберите класс:', reply_markup= markup_inline)

    if call.data == '5':
        buttons_five = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[0: 13:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'V')
            buttons_five.append(button)
        markup_inline.add(*buttons_five)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Выберите букву:', reply_markup=markup_inline)
        buttons_five.clear()

    if call.data == '6':
        buttons_six = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[13: 26:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'V')
            buttons_six.append(button)
        markup_inline.add(*buttons_six)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Выберите букву:', reply_markup=markup_inline)
        buttons_six.clear()

    if call.data == '7':
        buttons_seven = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[26: 35:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'V')
            buttons_seven.append(button)
        markup_inline.add(*buttons_seven)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Выберите букву:', reply_markup=markup_inline)
        buttons_seven.clear()

    if call.data == '8':
        buttons_8 = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[35: 45:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'V')
            buttons_8.append(button)
        markup_inline.add(*buttons_8)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Выберите букву:', reply_markup=markup_inline)
        buttons_8.clear()

    if call.data == '9':
        buttons_9 = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[45: 55:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'V')
            buttons_9.append(button)
        markup_inline.add(*buttons_9)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Выберите букву:', reply_markup=markup_inline)
        buttons_9.clear()

    if call.data == '10':
        buttons_10 = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[55: 59:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'V')
            buttons_10.append(button)
        markup_inline.add(*buttons_10)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Выберите букву:', reply_markup=markup_inline)
        buttons_10.clear()

    if call.data == '11':
        buttons_11 = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[59: 62:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'V')
            buttons_11.append(button)
        markup_inline.add(*buttons_11)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Выберите букву:', reply_markup=markup_inline)
        buttons_11.clear()

    def search(message):
        global teachersAll, teachersAllIds
        msg = message.text
        buttons_12 = []
        buttons_height = 10
        inline_2 = types.InlineKeyboardMarkup(row_width=2)
        for teacher in teachersAll:
            if msg.lower() in teacher.lower():
                button = types.InlineKeyboardButton(text=teacher, callback_data=teacher + 'G')
                buttons_12.append(button)
        if (buttons_12 != []):
            inline_2.add(*buttons_12)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Выберите учителя:', reply_markup=inline_2)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Учитель не найден(')

    def generate_keyboard():
        user_id = call.from_user.id
        conn = sqlite3.connect('ids.db')
        cur = conn.cursor()
        cur.execute('''SELECT page FROM users WHERE id = (?)''', (user_id,))
        page = int(cur.fetchone()[0])
        conn.commit()
        cur.close()
        conn.close()
        teachers = []
        buttons_height = 10
        inline = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text='⬅️', callback_data='back')
        next_button = types.InlineKeyboardButton(text='➡️', callback_data='next')
        search_button = types.InlineKeyboardButton(text='Найти учителя', callback_data='search')
        for teacher in teachersAll[buttons_height * (page - 1): page*buttons_height:]:
            teacher_but = button = types.InlineKeyboardButton(text=teacher, callback_data=teacher + 'G')
            teachers.append(teacher_but)
        inline.add(*teachers)
        inline.add(back_button, next_button)
        inline.add(search_button)
        return inline

    if call.data == 'back' and page != 1:
        user_id = call.from_user.id
        conn = sqlite3.connect('ids.db')
        cur = conn.cursor()
        cur.execute('''UPDATE users SET page = page - 1 WHERE id = (?)''', (user_id,))
        conn.commit()
        cur.execute('''SELECT page  FROM users WHERE id = (?)''', (user_id,))
        page = int(cur.fetchone()[0])
        conn.commit()
        cur.close()
        conn.close()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Выберите учителя: \nСтраница {page}', reply_markup=generate_keyboard())

    elif call.data == 'next':
        user_id = call.from_user.id
        conn = sqlite3.connect('ids.db')
        cur = conn.cursor()
        cur.execute('''UPDATE users SET page = page + 1 WHERE id = (?)''', (user_id,))
        conn.commit()
        cur.execute('''SELECT page  FROM users WHERE id = (?)''', (user_id,))
        page = int(cur.fetchone()[0])
        conn.commit()
        cur.close()
        conn.close()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Выберите учителя: \nСтраница {page}', reply_markup=generate_keyboard())

    elif call.data == 'search':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Напишите фамилию или начало фамилии учителя:')
        bot.register_next_step_handler(msg, search)

    if call.data == 'Teach':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите учителя:', reply_markup=generate_keyboard())

    def generate_keyboardG():
        user_id = call.from_user.id
        conn = sqlite3.connect('ids.db')
        cur = conn.cursor()
        cur.execute('''SELECT page FROM users  WHERE id = (?)''', (user_id,))
        page = int(cur.fetchone()[0])
        conn.commit()
        cur.close()
        conn.close()
        teachers = []
        buttons_height = 10
        inline = types.InlineKeyboardMarkup(row_width=2)
        back_button = types.InlineKeyboardButton(text='⬅️', callback_data='backH')
        next_button = types.InlineKeyboardButton(text='➡️', callback_data='nextH')
        for teacher in teachersAll[buttons_height * (page - 1): page*buttons_height:]:
            teacher_but = button = types.InlineKeyboardButton(text=teacher, callback_data=teacher + 'C')
            teachers.append(teacher_but)
        inline.add(*teachers)
        inline.add(back_button, next_button)
        return inline

    if call.data == 'backH' and page != 1:
        user_id = call.from_user.id
        conn = sqlite3.connect('ids.db')
        cur = conn.cursor()
        cur.execute('''UPDATE users SET page = page - 1 WHERE id = (?)''', (user_id,))
        cur.execute('''SELECT page FROM users WHERE id = (?)''', (user_id,))
        page = int(cur.fetchone()[0])
        conn.commit()
        cur.close()
        conn.close()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Выберите учителя: \nСтраница {page}', reply_markup=generate_keyboardG())

    elif call.data == 'nextH':
        user_id = call.from_user.id
        conn = sqlite3.connect('ids.db')
        cur = conn.cursor()
        cur.execute('''UPDATE users SET page = page + 1 WHERE id = (?)''', (user_id,))
        cur.execute('''SELECT page FROM users WHERE id = (?)''', (user_id,))
        page = int(cur.fetchone()[0])
        conn.commit()
        cur.close()
        conn.close()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Выберите учителя: \nСтраница {page}', reply_markup=generate_keyboardG())

    if call.data == 'TeachH':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите учителя:', reply_markup=generate_keyboardG())

    if call.data[-1] == 'V':
        conn = sqlite3.connect('ids.db')
        cur = conn.cursor()
        user_id = call.from_user.id
        cur.execute("""UPDATE users SET class_name_temp = ? WHERE id = ?""", (call.data[:-1], user_id))
        conn.commit()
        cur.close()
        conn.close()
        next_message_rasp(call)

    if call.data[-1] == 'G':
        conn = sqlite3.connect('ids.db')
        cur = conn.cursor()
        user_id = call.from_user.id
        cur.execute("""UPDATE users SET class_name_temp = ? WHERE id = ?""", (call.data[:-1], user_id))
        conn.commit()
        cur.close()
        conn.close()
        next_message_rasp_teach(call)


    def send_rasp(messages, selectDate, req, user_id):
        try:
            global teacher
            page = 1
            conn = sqlite3.connect('ids.db')
            cur = conn.cursor()
            selectDate = selectDate.strftime('%Y-%m-%d')
            cur.execute(f'''SELECT schedule_form FROM users WHERE id = {user_id}''')
            schedule_form = str(cur.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
            cur.execute(f'''SELECT teacher_exist FROM users WHERE id = {user_id}''')
            teacher_exist = str(cur.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
            if teacher_exist == 'None':
                cur.execute('UPDATE users SET teacher_exist = ? WHERE id = ?', (1, user_id))
                teacher_exist = '1'

            if schedule_form == 'None':
                cur.execute('UPDATE users SET schedule_form = ? WHERE id = ?', (1, user_id))
                schedule_form = '1'

            if req == 0:
                cur.execute("SELECT class_id FROM classes WHERE class_name = (SELECT class_name_temp FROM users WHERE id = ?)", (user_id,))
                selectGroup = cur.fetchall()
                selectGroup = str(selectGroup)
                selectGroup = selectGroup.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
                params = {
                    'selectGroup': selectGroup,
                    'selectTeacher': '222',
                    'selectPlace': '174',
                    'selectDate[]': selectDate,
                    'type': 'group'
                }

            elif req == 1:
                cur.execute("SELECT teacher_id FROM teachers WHERE teacher_name = (SELECT class_name_temp FROM users WHERE id = ?)", (user_id,))
                selectTeacher = cur.fetchall()
                selectTeacher = str(selectTeacher)
                selectTeacher = selectTeacher.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
                cur.execute(f'''SELECT schedule_form FROM users WHERE id = {user_id}''')
                params = {
                    'selectGroup': '215',
                    'selectTeacher': selectTeacher,
                    'selectPlace': '174',
                    'selectDate[]': selectDate,
                    'type': 'teacher'
                }

            conn.commit()
            cur.close()
            conn.close()
            response = requests.get(url, params=params)
            data_str = response.json()
            data = json.loads(data_str)
            if schedule_form == '1':
                message = []
                for item in data[0]:
                    for lesson in item:
                        if teacher_exist == '1':
                            if req == 0:
                                message.append(lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["teacher"] + ' | ' + lesson["place"])
                            else:
                                message.append(lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["group"] + ' | ' + lesson["place"])
                        elif teacher_exist == '0':
                            message.append(lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["place"])
                createImage(message, messages.chat.id, teacher_exist)
                with open(f'img/table{messages.chat.id}.jpg', 'rb') as photo:
                    bot.delete_message(messages.chat.id, messages.message_id)
                    bot.send_photo(messages.chat.id, photo, selectDate)
            else:
                message = ''
                for item in data[0]:
                    for lesson in item:
                        if teacher_exist == '1':
                            if req == 0:
                                message += lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["teacher"] + ' | ' + lesson["place"] + '\n' + '-' + '\n'
                            else:
                                message += lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["group"] + ' | ' + lesson["place"] + '\n' + '-' + '\n'
                        elif teacher_exist == '0':
                            if req == 0:
                                message += lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["teacher"] + ' | ' + lesson["place"] + '\n' + '-' + '\n'
                            else:
                                message += lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["group"] + ' | ' + lesson["place"] + '\n' + '-' + '\n'
                bot.edit_message_text(chat_id = messages.chat.id, message_id = messages.message_id, text = f'Расписание на {selectDate}\n{message}')
        except IndexError:
            bot.edit_message_text(chat_id=messages.chat.id, message_id=messages.message_id, text='Расписание ещё не выложили!')


    if call.data == 'Сегодня':
        send_rasp(call.message, datetime.datetime.now(), 0, call.from_user.id)


    elif call.data == 'Завтра':
        selectDate = datetime.datetime.now()
        selectDate = selectDate + datetime.timedelta(days=1)
        send_rasp(call.message, selectDate, 0, call.from_user.id)

    if call.data == 'СегодняTE':
        send_rasp(call.message, datetime.datetime.now(), 1, call.from_user.id)


    elif call.data == 'ЗавтраTE':
        selectDate = datetime.datetime.now()
        selectDate = selectDate + datetime.timedelta(days=1)
        send_rasp(call.message, selectDate, 1, call.from_user.id)


    def edit_settings():
        conn = sqlite3.connect('ids.db')
        cur = conn.cursor()
        usid = call.from_user.id
        cur.execute(f'SELECT class_name FROM users WHERE id = {usid}')
        rows = cur.fetchall()
        clas = f'{rows}'
        clas = clas.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("'", "").replace("'", "").replace(",", "")
        cur.execute(f'SELECT teacher_exist FROM users WHERE id = {usid}')
        teacher_exist = cur.fetchall()[0][0]
        if teacher_exist == 0:
            teacher_exist = '🔴'
        else:
            teacher_exist = '🟢'
        cur.execute(f'SELECT autoSchedule FROM users WHERE id = {usid}')
        autoShedule = cur.fetchall()[0][0]
        if autoShedule == 0:
            autoShedule = '🔴'
        else:
            autoShedule = '🟢'
        cur.close()
        conn.close()
        if clas == '':
            changeClas(message)
            return
        m = types.InlineKeyboardMarkup()
        changeScheduleFormBut = types.InlineKeyboardButton('Дизайн расписания', callback_data='changeScheduleForm')
        changeTeacherExistBut = types.InlineKeyboardButton(f'{teacher_exist}учителя в расписании', callback_data='changeTeacherExist')
        changeAutoScheduleBut = types.InlineKeyboardButton(f'{autoShedule}Авто-расписание', callback_data='changeAutoSchedule')
        m.row(changeScheduleFormBut)
        m.row(changeTeacherExistBut)
        m.row(changeAutoScheduleBut)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Возможные опции:', reply_markup=m)


    if call.data == 'changeScheduleForm':
        conn = sqlite3.connect('ids.db')
        cur = conn.cursor()
        user_id = call.from_user.id
        cur.execute(f'''SELECT schedule_form FROM users WHERE id = {user_id}''')
        schedule_form = str(cur.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
        if schedule_form == '1':
            cur.execute('''UPDATE users SET schedule_form = ? WHERE id = ?''', (0, user_id))
            bot.send_message(call.message.chat.id, 'Ваш дизайн расписания был изменён на текст')
        else:
            cur.execute('''UPDATE users SET schedule_form = ? WHERE id = ?''', (1, user_id))
            bot.send_message(call.message.chat.id, 'Ваш дизайн расписания был изменён на таблицу')
        conn.commit()
        cur.close()
        conn.close()

    elif call.data == 'changeTeacherExist':
        conn = sqlite3.connect('ids.db')
        cur = conn.cursor()
        user_id = call.from_user.id
        cur.execute(f'''SELECT teacher_exist FROM users WHERE id = {user_id}''')
        schedule_form = str(cur.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
        if schedule_form == '1':
            cur.execute('''UPDATE users SET teacher_exist = ? WHERE id = ?''', (0, user_id))
        else:
            cur.execute('''UPDATE users SET teacher_exist = ? WHERE id = ?''', (1, user_id))
        conn.commit()
        cur.close()
        conn.close()
        edit_settings()

    elif call.data == 'changeAutoSchedule':
        conn = sqlite3.connect('ids.db')
        cur = conn.cursor()
        user_id = call.from_user.id
        cur.execute(f'''SELECT autoSchedule FROM users WHERE id = {user_id}''')
        autoSchedule = str(cur.fetchall()).replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
        if autoSchedule == '1':
            cur.execute('''UPDATE users SET autoSchedule = ? WHERE id = ?''', (0, user_id))
        else:
            cur.execute('''UPDATE users SET autoSchedule = ? WHERE id = ?''', (1, user_id))
        conn.commit()
        cur.close()
        conn.close()
        edit_settings()

    if call.data == '5P':
        buttons_five = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[0: 13:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'C')
            buttons_five.append(button)
        markup_inline.add(*buttons_five)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите букву:',
                              reply_markup=markup_inline)
        buttons_five.clear()

    elif call.data == '6P':
        buttons_six = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[13: 26:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'C')
            buttons_six.append(button)
        markup_inline.add(*buttons_six)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите букву:',
                              reply_markup=markup_inline)
        buttons_six.clear()

    elif call.data == '7P':
        buttons_seven = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[26: 35:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'C')
            buttons_seven.append(button)
        markup_inline.add(*buttons_seven)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите букву:',
                              reply_markup=markup_inline)
        buttons_seven.clear()

    elif call.data == '8P':
        buttons_8 = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[35: 45:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'C')
            buttons_8.append(button)
        markup_inline.add(*buttons_8)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите букву:',
                              reply_markup=markup_inline)
        buttons_8.clear()

    elif call.data == '9P':
        buttons_9 = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[45: 55:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'C')
            buttons_9.append(button)
        markup_inline.add(*buttons_9)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите букву:',
                              reply_markup=markup_inline)
        buttons_9.clear()

    elif call.data == '10P':
        buttons_10 = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[55: 59:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'C')
            buttons_10.append(button)
        markup_inline.add(*buttons_10)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите букву:',
                              reply_markup=markup_inline)
        buttons_10.clear()

    elif call.data == '11P':
        buttons_11 = []
        inline = types.InlineKeyboardMarkup(row_width=2)
        for clas in classesAll[59: 62:]:
            button = types.InlineKeyboardButton(text=clas, callback_data=clas + 'C')
            buttons_11.append(button)
        markup_inline.add(*buttons_11)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите букву:',
                              reply_markup=markup_inline)
        buttons_11.clear()

    elif call.data[-1] == 'C':
        id = call.from_user.id
        user_clas(call.message, call.data[:-1], id)


try:
    bot.infinity_polling(timeout=10, long_polling_timeout = 5, skip_pending=True)
except:
    bot.infinity_polling(timeout=10, long_polling_timeout = 5, skip_pending=True)
