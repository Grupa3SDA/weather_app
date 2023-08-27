from dataclasses import dataclass
from datetime import datetime


@dataclass
class WeatherData:
    time: str
    latitude: float
    longitude: float
    name: str
    country: str
    weather_icon: str
    temperature: float
    feels_like: float
    cloudiness: int
    weather_description: str
    wind_speed: float
    wind_deg: str
    pressure: int
    humidity: int
    visibility: int
    sunrise: str
    sunset: str

    @classmethod
    def from_raw_weather_data(cls, weather_data):
        wind_deg = weather_data['wind']['deg']
        cardinal_directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                               'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        wind_deg = cardinal_directions[int((wind_deg + 11.25) / 22.5) % 16]
        time = datetime.now().strftime('%b %I:%M %p')
        return cls(
            time=time,
            latitude=weather_data['coord']['lat'],
            longitude=weather_data['coord']['lon'],
            name=weather_data['name'],
            country=weather_data['sys']['country'],
            weather_icon=weather_data['weather'][0]['icon'],
            temperature=round(weather_data['main']['temp'], 1),
            feels_like=round(weather_data['main']['feels_like'], 1),
            cloudiness=weather_data['clouds']['all'],
            weather_description=weather_data['weather'][0]['description'],
            wind_speed=weather_data['wind']['speed'],
            wind_deg=wind_deg,
            pressure=weather_data['main']['pressure'],
            humidity=weather_data['main']['humidity'],
            visibility=weather_data.get('visibility', 0),
            sunrise=datetime.utcfromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S'),
            sunset=datetime.utcfromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S'),
        )


@dataclass
class ForecastData:
    date: str
    time: str
    weather_icon: str
    cloudiness: int
    weather_description: str
    temp_max: str
    temp_min: str

    @classmethod
    def from_raw_forecast_data(cls, forecast_data):
        forecasts_by_date = {}
        time_map = {
            '00:00:00': 'Midnight',
            '03:00:00': 'Late Night',
            '06:00:00': 'Early Morning',
            '09:00:00': 'Morning',
            '12:00:00': 'Noon',
            '15:00:00': 'Afternoon',
            '18:00:00': 'Evening',
            '21:00:00': 'Late Evening'
        }
        for forecast in forecast_data['list']:
            dt_txt = forecast['dt_txt']
            date, time = dt_txt.split(' ')
            time = time_map[time]
            weather_icon = forecast['weather'][0]['icon']
            temp_max = round(forecast['main']['temp_max'], 1)
            temp_min = round(forecast['main']['temp_min'], 1)
            cloudiness = forecast['clouds']['all']
            weather_description = forecast['weather'][0]['description']
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            day_name = date_obj.strftime('%a, %b %d')

            if day_name not in forecasts_by_date:
                forecasts_by_date[day_name] = []

            forecasts_by_date[day_name].append(cls(
                date=day_name,
                time=time,
                weather_icon=weather_icon,
                temp_max=temp_max,
                temp_min=temp_min,
                cloudiness=cloudiness,
                weather_description=weather_description
            ))
        return forecasts_by_date


@dataclass
class AirPollutionData:
    aqi: int
    co: int
    no: int
    no2: int
    o3: int
    so2: int
    pm2_5: int
    pm10: int
    nh3: int

    @classmethod
    def from_raw_air_pollution_data(cls, air_pollution_data):
        return cls(
            aqi=air_pollution_data["list"][0]["main"]["aqi"],
            co=air_pollution_data['list'][0]['components']["co"],
            no=air_pollution_data['list'][0]['components']["no"],
            no2=air_pollution_data['list'][0]['components']["no2"],
            o3=air_pollution_data['list'][0]['components']["o3"],
            so2=air_pollution_data['list'][0]['components']["so2"],
            pm2_5=air_pollution_data['list'][0]['components']["pm2_5"],
            pm10=air_pollution_data['list'][0]['components']["pm10"],
            nh3=air_pollution_data['list'][0]['components']["nh3"],
        )
