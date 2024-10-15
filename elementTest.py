import requests
from datetime import datetime, timedelta


API_KEY = 'd9939ac907510bade3af110d9b0b91f1'
CITY = 'Череповец'
url = f'http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric&lang=ru'
response = requests.get(url)
data = response.json()
tomorrow = datetime.now() + timedelta(days=1)
tomorrow_date = tomorrow.strftime('%Y-%m-%d')
for forecast in data['list']:
    forecast_date = forecast['dt_txt'].split()[0]
    if forecast_date == tomorrow_date:
        temperature = forecast['main']['temp']
        description = forecast['weather'][0]['description']
        print(f"Прогноз погоды на завтра:\nТемпература: {temperature}°C\nОписание: {description}")
        break