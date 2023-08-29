from django.shortcuts import render
from requests.exceptions import HTTPError

from .forms import CityFormForWeather
from .services import WeatherService


def weather_and_forecast_view(request):
    city_form = CityFormForWeather(request.POST or None)
    context = {'city_form': city_form}
    if request.method == 'POST' and city_form.is_valid():
        city_name = city_form.cleaned_data['city_name']
        weather_service = WeatherService(city_name)
        try:
            weather_service.get_weather_and_foreacst()
            context.update({
                'city_name': city_name,
                'weather_data': weather_service.weather_data,
                'forecast_data': weather_service.forecast_data,
            })
        except HTTPError as e:
            if e.response.status_code >= 500:
                error_message = "External API error, please try again later or contact your site administrator."
                context.update({'error': error_message})
            elif e.response.status_code == 404:
                error_message = "City not found in API database, check name and try again."
                context.update({'error': error_message})
            else:
                raise e

    return render(request, "weather_and_forecast.html", context)
