import datetime
import time
import requests
import schedule


def raspcheck():
    try:
        selectGroup = '248'
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
        bot.send_message(users, 'расписание обновилось!')
        selectDate = datetime.datetime.now()
    except NameError:
        print('N')
        pass

schedule.every(5).seconds.do(raspcheck)
    schedule.run_pending()





