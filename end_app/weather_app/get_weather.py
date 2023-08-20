import requests
import os
from dotenv import load_dotenv
from datetime import datetime

def get_weather_data(city_name):
    load_dotenv()
    api_key = os.getenv("api_key")
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}'

    response = requests.get(base_url)
    data = response.json()

    # Pobranie dodatkowych informacji (przykładowe pola, może być inaczej z API)
    additional_info = {
        'cloudiness': data['clouds']['all'],
        'sunrise': datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
        'sunset': datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S'),
        'visibility': data.get('visibility', 'N/A'),
        'uvi': data.get('uvi', 'N/A'),
        'aqi': data.get('main', {}).get('aqi', 'N/A'),
        'weather_description': data['weather'][0]['description'],
        'weather_icon': data['weather'][0]['icon'],
        'temperature': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'temp_min': data['main']['temp_min'],
        'temp_max': data['main']['temp_max'],
        'pressure': data['main']['pressure'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed'],
        'wind_deg': data['wind']['deg'],
        'rain_1h': data.get('rain', {}).get('1h', 0),
        'rain_3h': data.get('rain', {}).get('3h', 0),
        'snow_1h': data.get('snow', {}).get('1h', 0),
        'snow_3h': data.get('snow', {}).get('3h', 0),
    }

    # Dodaj dodatkowe informacje do danych pogodowych
    data['additional_info'] = additional_info

    return data



