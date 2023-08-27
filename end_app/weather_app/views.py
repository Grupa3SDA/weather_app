from django.shortcuts import render
from requests import HTTPError

from .forms import CityForm
from .get_weather import get_weather_data, get_forecast_data, get_air_pollution_data
from .utils import Weather, Forecast, AirPollution


def weather(request):
    city_form = CityForm(request.POST or None)
    city_name = None
    weather_model = None
    forecast_model = None
    air_pollution_model = None

    if city_form.is_valid():
        city_name = city_form.cleaned_data["city_name"]

        try:
            weather_data = get_weather_data(city_name)
            weather_model = Weather.from_weather_data(weather_data)
            latitude = weather_model.latitude
            longitude = weather_model.longitude
            forecast_data = get_forecast_data(latitude, longitude)
            forecast_model = Forecast.from_forecast_data(forecast_data)
            air_pollution_data = get_air_pollution_data(latitude, longitude)
            air_pollution_model = AirPollution.from_air_pollution_data(air_pollution_data)

        except HTTPError as e:
            if e.response.status_code >= 500:
                error_message = "API error, please try again later or contact with site administrator."
            elif e.response.status_code == 404:
                error_message = "No city found in the database, please check the name and try again."
            else:
                error_message = {"error": str(e)}

            return render(request, "weather.html", error_message)

    context = {
        "city_form": city_form,
        "city_name": city_name,
        "weather_model": weather_model,
        "forecast_model": forecast_model,
        "air_pollution_model": air_pollution_model,
    }

    return render(request, "weather.html", context)
