from .get_weather import get_weather, get_forecast, get_air_pollution


class DataView:
    def __init__(self, city_name):
        self.city_name = city_name
        self.weather_data = None
        self.forecast_data = None
        self.air_pollution_data = None
        self.error_message = None
        self.latitude = None
        self.longitude = None

        if self.city_name is not None:
            self.weather_data, self.latitude, self.longitude, self.error_message = get_weather(self.city_name)
            if self.weather_data is not None:
                self.forecast_data, error_message = get_forecast(self.latitude, self.longitude)
                if error_message is not None:
                    self.error_message = error_message
                self.air_pollution_data, error_message = get_air_pollution(self.latitude, self.longitude)
                if error_message is not None:
                    self.error_message = error_message
