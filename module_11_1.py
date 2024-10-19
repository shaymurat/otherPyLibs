''' Выводит прогноз погоды на три дня, используя сервис open-meteo.com
Местоположение определяется по IP через сервис ip2location.io
'''

import requests


def direction(degrees: float) -> str:
    '''переводит азимут в розу ветров'''
    if degrees < 23:
        return "северный"
    elif degrees < 68:
        return "северо-восточный"
    elif degrees < 113:
        return "восточный"
    elif degrees < 158:
        return "юго-восточный"
    elif degrees < 203:
        return "южный"
    elif degrees < 248:
        return "юго-западный"
    elif degrees < 293:
        return "западный"
    elif degrees < 338:
        return "северо-западный"
    else:
        return "северный"


def print_daily_forecast(forecast: dict, i: int):
    print()
    print(('Завтра:', 'Послезавтра:', 'На 3-й день:')[i])
    print(f'Днём {forecast["temperature_2m_max"][i]}°C,',
          f'ночью {forecast["temperature_2m_min"][i]}°C,')
    print(f'Осадки {forecast["precipitation_sum"][i]} мм,',
          f'с вероятностью {forecast["precipitation_probability_mean"][i]}%')
    print('Ветер',
          f'{direction(float(forecast["wind_direction_10m_dominant"][i]))},',
          f'{forecast["wind_speed_10m_max"][i]} м/с')


GEO = 'https://api.ip2location.io/'
ERR_LOC = 'Не удалось определить ваше местонахождение'
ERR_MSG = 'Над всей Испанией безоблачное небо, a в Сантьяго идёт дождь'

print('Прогноз погоды')

geo_resp = requests.get(GEO)
if not geo_resp.ok:
    print(ERR_LOC)
    exit(1)
geo_json = geo_resp.json()
country = geo_json['country_name']
city    = geo_json['city_name']
lat     = geo_json['latitude']
long    = geo_json['longitude']
tz = 'auto'

METEO = 'https://api.open-meteo.com/v1/forecast'

daily = ('weather_code,'
         'temperature_2m_max,'
         'temperature_2m_min,'
         'precipitation_sum,'
         'precipitation_probability_mean,'
         'wind_speed_10m_max,'
         'wind_direction_10m_dominant')

params = {'latitude': lat,
          'longitude': long,
          'wind_speed_unit': 'ms',
          'timezone': tz,
          'forecast_days': '3',
          'daily': daily}

meteo_resp = requests.get(METEO, params=params)
if not meteo_resp.ok:
    print(ERR_MSG)
    exit(2)
forecast = meteo_resp.json()['daily']
print(f'{country}, {city}')
for i in range(3):
    print_daily_forecast(forecast, i)
