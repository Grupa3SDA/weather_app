from dataclasses import dataclass, fields
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
    co: float
    no: float
    no2: float
    o3: float
    so2: float
    pm2_5: float
    pm10: float
    nh3: float

    @classmethod
    def from_raw_air_pollution_data(cls, air_pollution_data):
        return cls(
            aqi=air_pollution_data["list"][0]["main"]["aqi"],
            co=round(air_pollution_data['list'][0]['components']["co"], 1),
            no=round(air_pollution_data['list'][0]['components']["no"], 1),
            no2=round(air_pollution_data['list'][0]['components']["no2"], 1),
            o3=round(air_pollution_data['list'][0]['components']["o3"], 1),
            so2=round(air_pollution_data['list'][0]['components']["so2"], 1),
            pm2_5=round(air_pollution_data['list'][0]['components']["pm2_5"], 1),
            pm10=round(air_pollution_data['list'][0]['components']["pm10"], 1),
            nh3=round(air_pollution_data['list'][0]['components']["nh3"], 1),
        )

    def get_scale_and_qualitative(self, value):
        if value == 'aqi':
            return '0-500', None
        elif value == 'co':
            if self.co < 4400:
                qualitative_name = 'Good'
            elif self.co < 9400:
                qualitative_name = 'Fair'
            elif self.co < 12400:
                qualitative_name = 'Moderate'
            elif self.co < 15400:
                qualitative_name = 'Poor'
            else:
                qualitative_name = 'Very Poor'
            return '0-15400μg/m3', qualitative_name
        elif value == 'no':
            if self.no < 100:
                qualitative_name = 'Good'
            else:
                qualitative_name = 'Very Poor'
            return '0-100ppb', qualitative_name
        elif value == 'no2':
            if self.no2 < 40:
                qualitative_name = 'Good'
            elif self.no2 < 70:
                qualitative_name = 'Fair'
            elif self.no2 < 150:
                qualitative_name = 'Moderate'
            elif self.no2 < 200:
                qualitative_name = 'Poor'
            else:
                qualitative_name = 'Very Poor'
            return '0-200ppb', qualitative_name
        elif value == 'o3':
            if self.o3 < 60:
                qualitative_name = 'Good'
            elif self.o3 < 100:
                qualitative_name = 'Fair'
            elif self.o3 < 140:
                qualitative_name = 'Moderate'
            elif self.o3 < 180:
                qualitative_name = 'Poor'
            else:
                qualitative_name = 'Very Poor'
            return '0-180ppb', qualitative_name
        elif value == 'so2':
            if self.so2 < 20:
                qualitative_name = 'Good'
            elif self.so2 < 80:
                qualitative_name = 'Fair'
            elif self.so2 < 250:
                qualitative_name = 'Moderate'
            elif self.so2 < 350:
                qualitative_name = 'Poor'
            else:
                qualitative_name = 'Very Poor'
            return '0-350ppb', qualitative_name
        elif value == 'pm2_5':
            if self.pm2_5 < 10:
                qualitative_name = 'Good'
            elif self.pm2_5 < 25:
                qualitative_name = 'Fair'
            elif self.pm2_5 < 50:
                qualitative_name = 'Moderate'
            elif self.pm2_5 < 75:
                qualitative_name = 'Poor'
            else:
                qualitative_name = 'Very Poor'
            return '0-75μg/m³', qualitative_name
        elif value == 'pm10':
            if self.pm10 < 20:
                qualitative_name = "Good"
            elif self.pm10 < 50:
                qualitative_name = "Fair"
            elif self.pm10 < 100:
                qualitative_name = "Moderate"
            elif self.pm10 < 200:
                qualitative_name = "Poor"
            else:
                qualitative_name = "Very Poor"
            return "0-200μg/m³", qualitative_name
        elif value == "nh3":
            if self.nh3 < 200:
                quantitative_value = "Good"
            else:
                quantitative_value = "Very Poor"
            return "0-200ppb", quantitative_value

    def to_list(self):
        result = []
        for field in fields(self):
            field_name = field.name
            value = getattr(self, field_name)
            scale, qualitative_name = self.get_scale_and_qualitative(field_name)
            if qualitative_name:
                result.append({"field_name": field_name, "value": value,
                               "scale": scale, "qualitative_name": qualitative_name})
            else:
                result.append({"field_name": field_name, "value": value, "scale": scale})
        return result

    def compare_air_quality(self, other):
        self_data = self.to_list()
        other_data = other.to_list()
        result = []
        for self_measurement, other_measurement in zip(self_data, other_data):
            field_name = self_measurement["field_name"]
            self_value = self_measurement["value"]
            other_value = other_measurement["value"]
            if self_value < other_value:
                comparison = "better in first city"
            elif self_value > other_value:
                comparison = "better in second city"
            else:
                comparison = "equal in both cities"
            result.append({"field_name": field_name, "comparison": comparison})
        return result
