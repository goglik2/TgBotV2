import telebot
from telebot import types
import requests
import json
import datetime
import threading
import sqlite3
from telebot import apihelper
import time


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
teachersAll = ['Тучанская В.В.', 'Андриевская Н.И.', 'Логинова О.П.', 'Борзенина М.А.', 'Цыб Т.В.', 'Морозова Ю.А.', 'Петренко Н.С.', 'Коротких А.И.', 'Пилостаева А.О.', 'Некрасова Н.В.', 'Семушина И.Л.', 'Тараторина О.В.', 'Шилова В.А.', 'Стрелкова М.А.', 'Кубык К.Р.', 'Попова М.С.', 'Синева Т.А.', 'Санникова Е.А.', 'Кашина А.Ю.', 'Корнилова В.В.', 'Абрамова Н.С.', 'ВздороваТ.С./Коробов А.В.', 'Илларионова В.П.', 'Антонова В.П./Тихомирова Н.С.', 'Коргинова А.В.', 'Павлова Я.М.', 'Горбунова М.А.', 'Ларчина Т.В.', 'Соколова Е.Е.', 'Семочкина А.А.', 'Ципилева Т.А.', 'Шевченко А.А.', 'Фёдорова К.Р.', 'Бесова Л.А.', 'Бокарева А.А.', 'Горбатович А.А.', 'Аверина К.Е./Скребцова И.А.', 'Рябкова С.Н.', 'Джанасова Н.Н.', 'Кистанова Н.Л.', 'Крылова Т.В.', 'Пелевина Н.В.', 'Гаджиева М.Г.', 'Яичкова М.М.', 'Каронова С.Г.', 'Филиппова Т.В.', 'Савинова К.В.', 'Комарова Л.А.', 'Бурмистрова О.Ю.', 'Крутикова Я.В.', 'Мокина И.Р.', 'Царева М.А.', 'Савина И.В.', 'Кузнецова М.А.', 'Самсонова Т.М.', 'Костина М.В.', 'Хонина Е.А.', 'Панина Е.В.', 'Петровичева А.А.', 'Божко А.А.', 'Балакшин Р.Н.', 'Мащенка П.А.', 'Богданова Е.В.', 'Ананьина И.К.', 'Григорьева Д.А.', 'Алексеева Т.В.', 'Груздева И.Н.', 'Проскурина Е.Н.', 'Постникова О.В.', 'Гаврилова Н.Н.', 'Галова А.В', 'Смирнова Е.А.', 'Ильиных И.В.', 'Новичихина Т.С.', 'Патютько Е.А.', 'Гордеев М.А.', 'Коршунова Р.С.', 'Харчева Е.Н.', 'Соболева И.С.', 'Соболева Е.А.', 'Чистякова Ю.О.', 'Лебедева Т.В.', 'Флегантова Н.С.', 'Лясникова Н.Д.', 'Корзина Ю.В.', 'Караваева В.А.', 'Ананьина О.Н.', 'Горинова Д.В.', 'Васильев И.Н.', 'Щерба Е.Ю.', 'Першичева Е.В.', 'Петрова В.О.', 'Агеева Л.Г.', 'Матвева Е.А.', 'Туницкая О.Ю.', 'Гаврилова О.В.', 'Репкина А.В.', 'Елисеева О.Г.', 'Савинова О.В.', 'Заборихина Ю.Л.', 'Ярулина В.Р.', 'Васильева С.Н.', 'Мащенко П.А.', 'Кириллов А.А./Божко А.А.', 'Соболева А.Н.', 'Куражова Н.Ю.', 'Иванова С.Г./Божко А.А.', 'Галова А.В.', 'Синицына А.Н.', 'Федорова Л.В.', 'Манаев И.А.', 'Матвеева Е.А.', 'Громова Т.В.', 'Юсуфович С.А.', 'Смирнова В.А.', 'Лисоцкова О.Н.', 'Борзунова Ю.А.', 'Ситников П.Л.', 'Трифанова М.С.', 'Горушкина А.В.', 'Неизвестно', 'Калиняк Л.В.', 'Добровольский Е.С.', 'Иванова С.Г.', 'Коробов А.В.', 'Байрамова Л.С.', 'Смирнова В.А.:3', 'Николаева Т.В./Истоцкая Н.Н.', 'Божко А.А./Кириллов А.А.', 'Божко А.А./Иванова С.Г.', 'Ефипова М.П.', 'Кронштатова Е.А.', 'Неизвестно ', 'Булычева Н.Н./Полубабкина Л.Г.', 'Костина М.В. ', 'Хонина Е.А. ', 'Чистякова Ю.О. ', 'Постникова О.В. ', 'Юсуфович С.А. ', 'Смирнова В.А. ', 'Смирнова Е.А. ', 'Байрамова Л.С. ', 'Заборихина Ю.Л. ', 'Першичева Е.В. ', 'Федорова Л.В. ', 'Галова А.В. ,', 'Лебедева Т.В. ', 'Репкина А.В. ', 'Новичихина Т.С. ', 'Калиняк Л.В. ', 'Синицина А.Н.', 'Постникова О.В.,', 'Галова А.В.,', 'Зона релаксации', 'Табунов И.А.', 'Глухова О.А.', 'Неизвестоно', 'Горинава Д.В.', 'Неизветно', 'Кириллов А.А.', 'Качкина А.Н.', 'Фёдоров М.Д.', 'Неклюдова Е.А.', 'Кукушкина А.А.', 'Коробов А.В.:', 'Фёдорова М.Д.', 'Белякова О.С.', 'Семушина И.А.', 'Смирнов А.А.', 'Английский язык', 'Геометрия', 'Большой', 'Разлетова В.В.', 'Булычева Н.Н.Полубабкина Л.Г.', 'Божко А.А.Иванова С.Г.', 'в/у "Разговоры о важном"', 'Электив Практическая география', 'Биология', 'Разлетова В.В.         ', 'Корзина Ю.В.   ', 'Чистякова Ю.О', 'Заборихина Ю.Л', 'Костина М.В', 'Хонина Е.А', 'Коршунова Р.С', 'Постникова О.В', 'Смирнова Е.А', 'Юсуфович С.А', 'Смирнова В.А', 'Байрамова Л.С', 'Ефипова М.П', 'Першичева Е.В', 'Федорова Л.В', 'Манаев И.А', 'Лебедева Т.В', 'Агеева Л.Г', 'Борзунова Ю.А', 'Репкина А.В', 'Фотосъёмка для летописи школы', 'Алгебра', 'Литература', 'География', 'Электив Биология в задачах', '/в/д "Математический практикум"', 'АКР по руссому языку', 'Информатика', 'Неизвестно.', 'Профтестирование', 'Манаев', '15.00-16.00', '12.00-13.00', '13.00-14.00', '14.00-15.00', 'Разлетова В.В.   ', 'Стеценко Н.Д.', 'Разлетова В.В', 'Калиняк Л.Г.', '        Разлетова В.В. ', 'Кривоборская Виктория Александровна.', 'Корзникова Юлия Сергеевна ', '/Федорова Л.В.', 'Ученые - в школы                         ', 'Разлетова В.В  ', 'Завьялова А.Н.', '/Коршунова Р.С.', 'ВПР география', 'м', '/Английский язык', 'Малый актовый зал', 'Немецкий язык', '/Немецкий язык', 'Иванова С.Г.     ', 'Божко А.А. ', 'Иванова С.Г.     /классный час', 'Иванова С.Г.     /зона релаксации', 'АКР по русскому языку', '/Галова А.В.', '   Классный час         А204(Р.яз)', 'Русский язык', 'Химия', 'АКР по математике        ', 'АКР по математике    ', 'АКР по математике             ', 'Ефипова М.П. А306(ин.яз)', '/Информатика', 'Родная литература', 'в/д "Математика в вопросах и ответах"', 'Постникова О.В..', 'Смирнова В.А..', 'Постникова О.В./Постникова О.В.', 'Феофанова Е.А.', 'Нетзвсетно', 'Консультация по химии Гаврилова О.В. Г2', 'Консультация по информатике Манаев И.А./Смирнова Е.А. Г104.1/Г104', 'Консультация по русскому языку Щерба Е.Ю. дистанционно', 'Щерба Е.Ю. Дистанционно', 'Консультация по математике Елисеева О.Г. Большой читальный зал', 'Консультация по русскому языку Ананьина О.Н. Г204', 'Консультация по математике 1п/гр Петрова В.О. Б142(ОБЖ)', 'Консультация по обществознанию Лясникова Н.Д. Г2', 'Горелова А.В.', 'Мелкова Е.Ю.', 'Твердохлеб К.', 'Кушева Т.А.', 'Елмалджиди Е.Г.', 'Крыскина К.А.', 'Истоцкая Н.Н.', 'Истоцкая Н.Н./Николаева Т.В.', 'Николаева Т.В.', 'Нестерова В.И.', 'Кочуева А.С.', 'Мартынов П.С.', 'Щукина О.И.', 'Калёва В.В.', 'Череповецкий Н.З.', 'Коковкина Е.С.', 'Востокова А.С.', 'Ситникова Я.В.', 'Шведова А.А.', 'Вакансия ин.яз', 'Андреева А.С.', 'Кумбула М.С.', 'Вакансия 1 кл', 'Агапова М.М.', 'Булычева А.А.', 'Куракина О.Г.', 'Коптяева О.А.', 'Короглуева А.И.', 'Кузнецова Е.И.', 'Петяева А.В.', 'Угрюмова В.И.', 'Мартынив А.И.', 'Тихомирова Н.С./Антонова В.П.', 'Черняева С.Е.', 'Кривоборская В.А.', 'Скребцова И.А. /Саругланова Ш.З.', 'Фомина Ю.И./Вакансия', 'Корзникова Ю.С.', 'Вздорова Т.С./Фомина Ю.И.', 'Лебедева Ю.А.', 'Елмаджиди Е.Г.', 'Курникова П.В.', 'Федорова К.Р.', 'Овчинникова Т.В.', 'Зона', 'Першичева Е.', 'Фомина Ю.И.', 'Большой актовый зал', 'Фомина Ю.И..', 'Николаева Т.В./Николаева Т.В.', 'Иванова С.Г../Иванова С.Г.', 'Иванова С.Г./Иванова С.Г.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'Коркина Н.А.', ' ', '', ' ', ' ', ' ', ' ', ' ', '.', ' ', ' ', 'Большой читальный зал-Г104.3', ' ', ' ', 'Истоцкая Н.Н./Истоцкая Н.Н.', 'Калева В.В.', 'Хребтова А.Р.', 'Белякова О.С. ', ' Белякова О.С. А205(р.яз)', 'Твердохлеб К.:', 'Першичева Е.В.:', 'Чистякова Ю.О.:', 'Щукина О.И.:', 'Хонина Е.А.:', 'Заборихина Ю.Л.:', 'Постникова О.В.:', 'Ефипова М.П.:', 'Галова А.В.:', 'Смирнова Е.А.:', 'Лебедева Т.В.:', 'Федорова Л.В.:', 'Байрамова Л.С.:', 'Г104.3-читальный зал', 'Мащенко М.П.', 'Юный Инженер', 'Божко А.А. (девочки)', 'Караваева В.А., Лисоцкова О.Н.', 'Иванова С.Г.(мальчики)', 'ГориноваД.В.', '/Электив Химия: от простого к сложному', 'Юноши 2007 г.р.', 'Юноши 2007 г.р. ', '/Профтестирование(военкомат) Юноши 2007 г.р.', 'военкомат', 'История', '/', 'Профтестирование(военкомат) Юноши 2007 г.р.', 'Иванова Е.А.', 'Мухина Л.Н.', 'Соколова И.В.', 'Божко А.А.(девочки)/(мальчики)', 'Божко А.А./Божко А.А.', 'Божко А.А.(девочки)', 'Сулейманова А.В.', 'Сулейманова В.А.', 'Зона релсакации', 'зона релаксации', 'Харчева Е.А.', 'Горелова А.В', 'Панина Е.В./Гаврилова Н.Н.', 'Куражова Н.Ю./Матвеева Е.А.', 'Петровичева А.А./Корзина Ю.В.', 'Богданова Е.В./Смирнова Е.А.', 'Харчева Е.Н./Лебедеа Т.В.', 'Электив История: теория и практика Караваева В.А. дистанционно', 'Агеева А.Г  ', 'Истоцкая Н.Н.(девочки)', 'Николаева Т.В.(мальчики)', 'Крыскина К. А.', 'Коркина Н.А..', 'Шешуев Г.А.', 'Базовая И.Ю.', 'Торочкова А.А.', 'Ключникова К.А.', 'Сергеева А.Д.', 'Классный час', 'Вакансия Био', 'Малинина Д.А.', 'Мокина А.М.', 'Мурашкина С.В., Мухина Л.Н.', 'Мокина А.М', 'Мокина А.В.', 'Обществознание', '/Электив Компьютерная грамотност', 'Электив Химия: от простого к сложному', 'Чистякова Ю.О.:3', 'Твердохлеб К.К.', 'Чистякова Ю.О..', 'Истоцкая Н.Н.(обе группы)', 'Истоцкая Н.Н.(только группа Истоцкой Н.Н.)', 'Мурашкина С.В.', 'Истоцкая Н.Н.(только группа Истоцкой Н.Н.', 'Горинова Д.В', 'Смирнова К.В.', 'Истоцкая Н.Н.(обе группы.)', 'Ситников П.С.']


global teachersAllIds
teachersAllIds = ['222', '223', '224', '225', '226', '227', '228', '229', '230', '231', '232', '233', '234', '235', '236', '237', '238', '239', '240', '241', '242', '243', '244', '245', '246', '247', '248', '249', '250', '251', '252', '253', '254', '255', '256', '257', '258', '259', '260', '261', '262', '263', '264', '265', '266', '267', '268', '269', '270', '271', '272', '273', '274', '275', '276', '277', '278', '279', '280', '281', '282', '283', '284', '285', '286', '287', '288', '289', '290', '291', '292', '293', '294', '295', '296', '297', '298', '299', '300', '301', '302', '303', '304', '305', '306', '307', '308', '309', '310', '311', '312', '313', '314', '315', '316', '317', '318', '319', '320', '321', '322', '323', '324', '325', '326', '327', '328', '329', '330', '331', '332', '333', '334', '335', '336', '337', '338', '339', '340', '341', '342', '344', '345', '346', '348', '351', '354', '355', '356', '358', '359', '360', '361', '363', '366', '367', '368', '369', '371', '372', '373', '374', '376', '377', '378', '379', '380', '381', '382', '383', '384', '385', '387', '392', '393', '394', '395', '396', '397', '399', '400', '401', '402', '403', '404', '405', '408', '409', '412', '413', '414', '415', '416', '417', '418', '420', '427', '428', '432', '433', '434', '435', '436', '437', '438', '439', '440', '441', '442', '443', '444', '445', '446', '447', '448', '449', '450', '451', '452', '453', '454', '455', '456', '457', '458', '459', '460', '461', '462', '463', '464', '465', '466', '467', '468', '469', '470', '471', '472', '473', '474', '475', '476', '477', '478', '479', '480', '481', '482', '483', '484', '485', '486', '487', '488', '489', '490', '491', '492', '493', '494', '495', '496', '497', '498', '499', '500', '501', '502', '503', '504', '505', '506', '507', '508', '509', '510', '511', '512', '513', '514', '515', '516', '517', '518', '519', '520', '521', '522', '523', '524', '525', '526', '527', '528', '529', '530', '531', '532', '533', '534', '535', '536', '537', '538', '539', '540', '541', '542', '543', '544', '545', '546', '547', '548', '549', '550', '551', '552', '553', '554', '555', '556', '557', '558', '559', '560', '561', '562', '563', '564', '565', '566', '567', '568', '569', '570', '571', '572', '573', '574', '575', '576', '577', '578', '579', '580', '581', '582', '583', '584', '585', '586', '587', '588', '589', '590', '591', '592', '593', '594', '595', '596', '597', '598', '599', '600', '601', '602', '603', '604', '605', '606', '607', '608', '609', '610', '611', '612', '613', '614', '615', '616', '617', '618', '619', '620', '621', '622', '623', '624', '625', '626', '627', '628', '629', '630', '631', '632', '633', '634', '635', '636', '637', '638', '639', '640', '641', '642', '643', '644', '645', '646', '647', '648', '649', '650', '651', '652', '653', '654', '655', '656', '657', '658', '659', '660', '661', '662', '663', '664', '665', '666', '667', '668', '669']

global url
url = 'https://rasp.milytin.ru/search'

bot = telebot.TeleBot('6873531488:AAFAHq3x42Blr7ckvwY2wppxVIutiyRWfP8')

@bot.message_handler(commands=['fif'])
def i6(m):
    print(m)


def checkRasp():
    while True:
        raspMes = False
        conn = sqlite3.connect('ids.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        cur.close()
        conn.close()
        infu = ''
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
        if data != []:
            for user in users:
                infu = f'{user[0]}'
                try:
                    bot.send_message(infu, 'Расписание обновилось!')
                    raspMes = True
                except:
                    continue
        if raspMes:
            raspMes = False
            time.sleep(50400)


#threading.Thread(target=checkRasp).start()


@bot.message_handler(commands=['postToAll23'])
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
            #classesinf += f'{classesi}\n'
            print(classesi)

        for teacher in teachers:
            print(teacher)

        bot.send_message(message.chat.id, f'Количество пользователей: {inf}')
        bot.send_document(message.chat.id, open(r'main.py', 'rb'))
        bot.send_document(message.chat.id, open(r'ids.db', 'rb'))
    else:
        bot.send_message(message.chat.id, f'Ты откуда это узнал?')


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, class_name TEXT, class_name_temp TEXT, page TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS classes (class_name TEXT, class_id TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS teachers (teacher_name TEXT, teacher_id TEXT)''')
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
        cur.execute('''INSERT INTO users (id, page) VALUES (?, ?)''', (user_id, 1))
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


def user_clas(message, clas, id):
    conn = sqlite3.connect('ids.db')
    cur = conn.cursor()
    cur.execute('SELECT id FROM users')
    userId = cur.fetchall()
    if id not in [x[0] for x in userId]:
        cur.execute('INSERT INTO users (id, class_name, page) VALUES (?, ?, ?)', (id, clas, 1))
        #threading.Thread(target=checkRasp, args=[id]).start()
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
    markup.row(btn1)
    markup.row(btn2, btn4)
    markup.row(btn3)
    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
    bot.send_message(message.chat.id, text = f'Список команд для этого бота:\n/start - перезапустить\n/help - список команд\n/rasp - Расписание\nВаш класс: {clas}', reply_markup=markup)


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
        bot.edit_message_text(chat_id = message.chat.id, message_id = message.message_id, text = 'Укажите ваш класс:', reply_markup=markup_inline)
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
    bot.send_message(chat_id = message.chat.id, text = f'Ваш класс: {clas}\nСписок команд для этого бота:\n/start - перезапустить\n/help - список команд\n/settings - поменять класс\n/rasp - Расписание')


@bot.message_handler(commands=['rasp'])
def rasp(message):
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
        bot.edit_message_text(chat_id = message.chat.id, message_id = message.message_id, text = 'Укажите ваш класс:', reply_markup=markup_inline)
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

    elif message.text.lower() == 'владимир путин':
        bot.send_message(message.chat.id, 'Молодец!\nПолитик, лидер и боец!')

    elif message.text.lower() == 'великолепно':
        bot.send_message(message.chat.id, 'В этот великолепный день, доделался этот великолепный бот, как-же это великолепно!')

    elif message.text.lower() == 'а':
        bot.send_message(message.chat.id, 'Двойку на!')

    elif message.text.lower() == 'да':
        bot.send_message(message.chat.id, 'Учиться пора!')

    elif message.text.lower() == 'опа':
        bot.reply_to(message, message.text)


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
        back_button = types.InlineKeyboardButton(text='←', callback_data='back')
        next_button = types.InlineKeyboardButton(text='→', callback_data='next')
        for teacher in teachersAll[buttons_height * (page - 1): page*buttons_height:]:
            teacher_but = button = types.InlineKeyboardButton(text=teacher, callback_data=teacher + 'G')
            teachers.append(teacher_but)
        inline.add(*teachers)
        inline.add(back_button, next_button)
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
        back_button = types.InlineKeyboardButton(text='←', callback_data='backH')
        next_button = types.InlineKeyboardButton(text='→', callback_data='nextH')
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
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = message)
        except IndexError:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Расписание ещё не выложили!')


    elif call.data == 'Завтра':
        try:
            selectDate = datetime.datetime.now()
            selectDate = selectDate + datetime.timedelta(days=1)
            selectDate = selectDate.strftime('%Y-%m-%d')
            conn = sqlite3.connect('ids.db')
            cur = conn.cursor()
            user_id = call.from_user.id
            cur.execute('''SELECT class_id FROM classes WHERE class_name = (SELECT class_name_temp FROM users WHERE id = ?)''', (user_id, ))
            selectGroup = cur.fetchall()[0]
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
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = message)
        except IndexError:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Расписание ещё не выложили!')

    if call.data == 'СегодняTE':
        try:
            page = 1
            selectDate = datetime.datetime.now()
            selectDate = selectDate.strftime('%Y-%m-%d')
            conn = sqlite3.connect('ids.db')
            cur = conn.cursor()
            user_id = call.from_user.id
            cur.execute("SELECT teacher_id FROM teachers WHERE teacher_name = (SELECT class_name_temp FROM users WHERE id = ?)", (user_id,))
            selectTeacher = cur.fetchall()
            selectTeacher = str(selectTeacher)
            selectTeacher = selectTeacher.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("'", "")
            conn.commit()
            cur.close()
            conn.close()
            params = {
                'selectGroup': '215',
                'selectTeacher': selectTeacher,
                'selectPlace': '174',
                'selectDate[]': selectDate,
                'type': 'teacher'
            }
            response = requests.get(url, params=params)
            data_str = response.json()
            data = json.loads(data_str)
            message = ''
            for item in data[0]:
                for lesson in item:
                    message += lesson["time"] + '\n' + lesson["discipline"] + ' | ' + lesson["group"] + ' | ' + lesson["place"] + '\n' + '-' + '\n'
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = message)
        except IndexError:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Расписание ещё не выложили!')


    elif call.data == 'ЗавтраTE':
        try:
            page = 1
            selectDate = datetime.datetime.now()
            selectDate = selectDate + datetime.timedelta(days=1)
            selectDate = selectDate.strftime('%Y-%m-%d')
            conn = sqlite3.connect('ids.db')
            cur = conn.cursor()
            user_id = call.from_user.id
            cur.execute(
                "SELECT teacher_id FROM teachers WHERE teacher_name = (SELECT class_name_temp FROM users WHERE id = ?)",
                (user_id,))
            selectTeacher = cur.fetchall()
            selectTeacher = str(selectTeacher)
            selectTeacher = selectTeacher.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(
                ",", "").replace("'", "").replace("'", "")
            conn.commit()
            cur.close()
            conn.close()
            params = {
                'selectGroup': '215',
                'selectTeacher': selectTeacher,
                'selectPlace': '174',
                'selectDate[]': selectDate,
                'type': 'teacher'
            }
            response = requests.get(url, params=params)
            data_str = response.json()
            data = json.loads(data_str)
            message = ''
            for item in data[0]:
                for lesson in item:
                    message += lesson["time"] + '\n' + lesson["discipline"] + ' | ' + lesson["group"] + ' | ' + lesson[
                        "place"] + '\n' + '-' + '\n'
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = message)
        except IndexError:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Расписание ещё не выложили!')


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