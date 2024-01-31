import requests
import json
import datetime
import time
import threading
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder
import aiohttp
from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


logging.basicConfig(level=logging.INFO)
bot = Bot('6873531488:AAFAHq3x42Blr7ckvwY2wppxVIutiyRWfP8')
dp = Dispatcher()


users = []
c_users = 0

joinedFile = open('ids.txt', 'r')
joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()

async def checkrasp(chat_id):
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
            await message.answer('Расписание обновилось!')
            time.sleep(50400)
        except IndexError:
            time.sleep(150)

with open('ids.txt', 'r') as joinedFile:
    joinedUsers = set(line.strip() for line in joinedFile)

for chat_id in joinedUsers:
    thr = threading.Thread(target=checkrasp, args=(chat_id,))
    thr.start()


@dp.message(Command('post23'))
async def post(message: types.Message):
    with open('ids.txt', 'r') as file:
        lines = file.readlines()

    unique_lines = set(lines)
    with open('ids.txt', 'w') as file:
        file.writelines(unique_lines)

    for user in joinedUsers:
        await message.answer(user, message.text[message.text.find(' '):])


@dp.message(Command('mg'))
async def mg(message: types.Message):
    with open('ids.txt', 'r') as file:
        lines = file.readlines()

    unique_lines = set(lines)
    with open('ids.txt', 'w') as file:
        file.writelines(unique_lines)

    joinedFile = open('ids.txt', 'r')
    await message.answer_document(joinedFile)
    joinedFile.close()


@dp.message(Command('start'))  #Команда для запуска бота и его стартовой функции
async def start(message: types.Message):
    if not str(message.chat.id) in joinedUsers:
        joinedFile = open('ids.txt', 'a')
        joinedFile.write(str(message.chat.id) + '\n')
        joinedUsers.add(message.chat.id)

    user_id = [message.from_user.first_name, message.from_user.last_name, message.from_user.username]            #Заполнение списка всех пользователей бота
    if user_id not in users:
        users.append(user_id)
        global c_users
        c_users += 1

    await message.answer(f'Приветсвую, {message.from_user.first_name}')
    kb = [
        [types.KeyboardButton(text='Расписание')],
        [types.KeyboardButton(text='Помощь')],
        [types.KeyboardButton(text='Перезапустить')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите нужную функцию'
    )
    await message.answer('Список команд для этого бота:\n/start - перезапустить\n/help - список команд\n/rasp - Расписание', reply_markup=keyboard)


@dp.message(Command('help'))        #при вводе команды help вылезает сообщение
async def info(message: types.Message):
    await message.answer(f'Список команд для этого бота:\n/start - перезапустить\n/help - список команд\n/rasp - Расписание')


@dp.message(Command('rasp'))
async def rasp(message: types.Message):
    kb = [
        [
            types.InlineKeyboardButton(text='5 класс', callback_data='5'),
            types.InlineKeyboardButton(text='6 класс', callback_data='6')
        ],
        [
            types.InlineKeyboardButton(text='7 класс', callback_data='7'),
            types.InlineKeyboardButton(text='8 класс', callback_data='8')
        ],
        [
            types.InlineKeyboardButton(text='9 класс', callback_data='9')
        ],
        [
            types.InlineKeyboardButton(text='10 класс', callback_data='10')
        ],
        [
            types.InlineKeyboardButton(text='11 класс', callback_data='11')
        ]
    ]
    builder = types.InlineKeyboardButton
    await message.answer('Выберите класс:',  reply_markup=builder.as_markup())


@dp.message(F.text.lower == 'расписание')
async def raspetext(message: types.message):
    asyncio.run(rasp(message))

@dp.message(F.text.lower == 'помощь')
async def raspetext(message: types.message):
    asyncio.run(info(message))

@dp.message(F.text.lower == 'помощь')
async def raspetext(message: types.message):
    await message.answer('Это Гриша сделал(и немного вова)')


@dp.message(F.text.lower == 'перезапустить')
async def raspetext(message: types.message):
    asyncio.run(start(message))

@dp.callback_query(F.data)
async def clasrasp(callback: types.CallbackQuery):
    global selectGroup
    builder = InlineKeyboardButton
    if call.data == '5':
        buttons = [
            [
                types.InlineKeyboardButton('5а', callback_data='5а'),
                types.InlineKeyboardButton('5б', callback_data='5б')
            ],
            [
                types.InlineKeyboardButton('5в', callback_data='5в'),
                types.InlineKeyboardButton('5г', callback_data='5г')

            ],
            [
                types.InlineKeyboardButton('5д', callback_data='5д'),
                types.InlineKeyboardButton('5е', callback_data='5е')
            ],
            [
                types.InlineKeyboardButton('5ж', callback_data='5ж'),
                types.InlineKeyboardButton('5з', callback_data='5з')
            ],
            [
                types.InlineKeyboardButton('5и', callback_data='5и'),
                types.InlineKeyboardButton('5к', callback_data='5к')
            ],
            [
                types.InlineKeyboardButton('5л', callback_data='5л'),
                types.InlineKeyboardButton('5м', callback_data='5м')
            ],
            [
                types.InlineKeyboardButton('5н', callback_data='5н')
            ]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard
        await message.answer(f'Выберите букву', reply_markup=builder.as_markup())


    elif call.data == '6':
        builder = types.InlineKeyboardMarkup()
        buttons = [
            [
                types.InlineKeyboardButton('6а', callback_data='6a'),
                types.InlineKeyboardButton('6б', callback_data='6б')
            ],
            [
                types.InlineKeyboardButton('6в', callback_data='6в'),
                types.InlineKeyboardButton('6г', callback_data='6г')

            ],
            [
                types.InlineKeyboardButton('6д', callback_data='6д'),
                types.InlineKeyboardButton('6е', callback_data='6е')
            ],
            [
                types.InlineKeyboardButton('6ж', callback_data='6ж'),
                types.InlineKeyboardButton('6з', callback_data='6з')
            ]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard
        await message.answer(f'Выберите букву', reply_markup=builder.as_markup())

    elif call.data == '7':
        builder = types.InlineKeyboardMarkup()
        buttons = [
            [
                types.InlineKeyboardButton('7а', callback_data='7а'),
                types.InlineKeyboardButton('7б', callback_data='7б')
            ],
            [
                types.InlineKeyboardButton('7в', callback_data='7в'),
                types.InlineKeyboardButton('7г', callback_data='7г')

            ],
            [
                types.InlineKeyboardButton('7д', callback_data='7д'),
                types.InlineKeyboardButton('7е', callback_data='7е')
            ],
            [
                types.InlineKeyboardButton('7ж', callback_data='7ж'),
                types.InlineKeyboardButton('7з', callback_data='7з')
            ]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard
        await message.answer(f'Выберите букву', reply_markup=builder.as_markup())

    elif call.data == '8':
        builder = types.InlineKeyboardMarkup()
        buttons = [
            [
                types.InlineKeyboardButton('8а', callback_data='8а'),
                types.InlineKeyboardButton('8б', callback_data='8б')
            ],
            [
                types.InlineKeyboardButton('8в', callback_data='8в'),
                types.InlineKeyboardButton('8г', callback_data='8г')

            ],
            [
                types.InlineKeyboardButton('8д', callback_data='8д'),
                types.InlineKeyboardButton('8е', callback_data='8е')
            ],
            [
                types.InlineKeyboardButton('8ж', callback_data='8ж'),
                types.InlineKeyboardButton('8з', callback_data='8з')
            ],
            [
                types.InlineKeyboardButton('8и', callback_data='8и'),
                types.InlineKeyboardButton('8к', callback_data='8к')
            ]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard
        await message.answer(f'Выберите букву', reply_markup=builder.as_markup())

    elif call.data == '9':
        builder = types.InlineKeyboardMarkup()
        buttons = [
            [
                types.InlineKeyboardButton('9а', callback_data='9а'),
                types.InlineKeyboardButton('9б', callback_data='9б')
            ],
            [
                types.InlineKeyboardButton('9в', callback_data='9в'),
                types.InlineKeyboardButton('9г', callback_data='9г')

            ],
            [
                types.InlineKeyboardButton('9д', callback_data='9д'),
                types.InlineKeyboardButton('9е', callback_data='9е')
            ],
            [
                types.InlineKeyboardButton('9ж', callback_data='9ж'),
                types.InlineKeyboardButton('9з', callback_data='9з')
            ],
            [
                types.InlineKeyboardButton('9и', callback_data='9и'),
                types.InlineKeyboardButton('9к', callback_data='9к')
            ]
        ]
        await message.answer(f'Выберите букву', reply_markup=builder.as_markup())

    elif call.data == '10':
        builder = types.InlineKeyboardMarkup()
        buttons = [
            [
                types.InlineKeyboardButton('10а', callback_data='10а'),
                types.InlineKeyboardButton('10б', callback_data='10б')
            ],
            [
                types.InlineKeyboardButton('10в', callback_data='10в')
            ]
        ]
        await message.answer(f'Выберите букву', reply_markup=builder.as_markup())

    elif call.data == '11':
        builder = types.InlineKeyboardMarkup()
        buttons = [
            [
                types.InlineKeyboardButton('11а', callback_data='11а'),
                types.InlineKeyboardButton('11б', callback_data='11б')
            ],
            [
                types.InlineKeyboardButton('11в', callback_data='11в')
            ]
        ]
        await message.answer(f'Выберите букву', reply_markup=builder.as_markup())

    if call.data == '5а':
        selectGroup = '212'

    elif call.data == '5б':
        selectGroup = '213'

    elif call.data == '5в':
        selectGroup = '214'

    elif call.data == '5г':
        selectGroup = '215'

    elif call.data == '5д':
        selectGroup = '216'

    elif call.data == '5е':
        selectGroup = '217'

    elif call.data == '5ж':
        selectGroup = '218'

    elif call.data == '5з':
        selectGroup = '219'

    elif call.data == '5и':
        selectGroup = '220'

    elif call.data == '5к':
        selectGroup = '268'

    elif call.data == '5л':
        selectGroup = '269'

    elif call.data == '5м':
        selectGroup = '270'

    elif call.data == '5н':
        selectGroup = '271'

    elif call.data == '6а':
        selectGroup = '221'

    elif call.data == '6г':
        selectGroup = '224'

    elif call.data == '6д':
        selectGroup = '225'

    elif call.data == '6е':
        selectGroup = '226'

    elif call.data == '6ж':
        selectGroup = '227'

    elif call.data == '6з':
        selectGroup = '228'

    elif call.data == '6б':
        selectGroup = '258'

    elif call.data == '6в':
        selectGroup = '259'

    elif call.data == '7а':
        selectGroup = '229'

    elif call.data == '7б':
        selectGroup = '230'

    elif call.data == '7в':
        selectGroup = '231'

    elif call.data == '7г':
        selectGroup = '232'

    elif call.data == '7д':
        selectGroup = '233'

    elif call.data == '7е':
        selectGroup = '260'

    elif call.data == '7ж':
        selectGroup = '273'

    elif call.data == '7з':
        selectGroup = '274'

    elif call.data == '8а':
        selectGroup = '235'

    elif call.data == '8б':
        selectGroup = '236'

    elif call.data == '8в':
        selectGroup = '237'

    elif call.data == '8г':
        selectGroup = '238'

    elif call.data == '8д':
        selectGroup = '239'

    elif call.data == '8е':
        selectGroup = '240'

    elif call.data == '8к':
        selectGroup = '244'

    elif call.data == '8ж':
        selectGroup = '261'

    elif call.data == '8з':
        selectGroup = '262'

    elif call.data == '8и':
        selectGroup = '263'

    elif call.data == '9а':
        selectGroup = '245'

    elif call.data == '9б':
        selectGroup = '246'

    elif call.data == '9в':
        selectGroup = '247'

    elif call.data == '9г':
        selectGroup = '248'

    elif call.data == '9д':
        selectGroup = '249'

    elif call.data == '9е':
        selectGroup = '250'

    elif call.data == '9ж':
        selectGroup = '264'

    elif call.data == '9з':
        selectGroup = '265'

    elif call.data == '9и':
        selectGroup = '266'

    elif call.data == '9к':
        selectGroup = '267'

    elif call.data == '10а':
        selectGroup = '251'

    elif call.data == '10б':
        selectGroup = '252'

    elif call.data == '10в':
        selectGroup = '253'

    elif call.data == '11а':
        selectGroup = '254'

    elif call.data == '11б':
        selectGroup = '255'

    elif call.data == '11в':
        selectGroup = '256'

    buttons = [
        [
            types.InlineKeyboardButton('Сегодня', callback_data='Сегодня')
        ],
        [
    types.InlineKeyboardButton('Завтра', callback_data='Завтра')
        ]
    ]
    await message.answer('Выберите дату', reply_markup=builder.as_markup())

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
                    await message.answer(lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["teacher"] + ' | ' + lesson["place"])
        except IndexError:
            await message.answer('Расписание ещё не выложили!')

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
                    await message.answer(lesson["time"] + ' | ' + lesson["discipline"] + ' | ' + lesson["teacher"] + ' | ' + lesson["place"])
        except IndexError:
            await message.answer('Расписание ещё не выложили!')

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())