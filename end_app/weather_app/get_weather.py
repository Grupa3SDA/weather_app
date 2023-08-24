import requests
from datetime import datetime
from end_app.settings import WEATHER_API_KEY
from end_app.settings import FORECAST_API_KEY
from end_app.settings import AIR_POLLUTION_API_KEY


def get_weather_data(city_name):
    weather_url = (f'https://api.openweathermap.org/data/2.5/weather?q={city_name}'
                   f'&units=metric&appid={WEATHER_API_KEY}')
    response = requests.get(weather_url)
    data = response.json()

    # error handling
    if response.status_code == 500:
        raise Exception("Internal server error in API")
    elif response.status_code == 404:
        return {'error': 'City not found'}
    elif response.status_code != 200:
        return {'error': 'Error fetching weather data'}

    # additional information from API that must be formatted
    additional_info = {
        'cloudiness': data['clouds']['all'],
        'sunrise': datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
        'sunset': datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S'),
        'visibility': data.get('visibility', 'N/A'),
        'uvi': data.get('uvi', 'N/A'),
        'aqi': data.get('aqi', 'N/A'),
        'rain_1h': data.get('rain', {}).get('1h', 0),
        'rain_3h': data.get('rain', {}).get('3h', 0),
        'snow_1h': data.get('snow', {}).get('1h', 0),
        'snow_3h': data.get('snow', {}).get('3h', 0),
    }

    # add formatted additional information to weather data
    data['additional_info'] = additional_info

    return data


def get_forecast_data(latitude, longitude):
    forecast_url = (f'https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}'
                    f'&units=metric&appid={FORECAST_API_KEY}')
    response = requests.get(forecast_url)
    data = response.json()

    return data


def get_air_pollution_data(latitude, longitude):
    air_polution_url = (f'https://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}'
                        f'&appid={AIR_POLLUTION_API_KEY}')
    response = requests.get(air_polution_url)
    data = response.json()

    return data
