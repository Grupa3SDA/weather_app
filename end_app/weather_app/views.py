from functools import wraps

from django.shortcuts import render
from requests.exceptions import HTTPError

from .forms import CityFormForWeather, CityFormForTwoCities
from .services import WeatherService


def handle_http_errors(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except HTTPError as e:
            context = {}
            city_form = CityFormForWeather(request.POST or None)
            context.update({'city_form': city_form})
            if 500 <= e.response.status_code <= 599:
                error_message = "External API error, please try again later or contact website service administrator."
                context.update({'error': error_message})
            elif e.response.status_code == 404:
                error_message = "City not found in API database, check name and try again."
                context.update({'error': error_message})
            elif e.response.status_code == 401 or e.response.status_code == 403:
                error_message = "Internal server error, please contact website service administrator."
                context.update({'error': error_message})
            elif e.response.status_code == 429:
                error_message = "Only 60 API calls per minute in our plan, please wait before your next search."
                context.update({'error': error_message})
            else:
                raise e
            return render(request, "weather_and_forecast.html", context)
    return wrapper


@handle_http_errors
def weather_and_forecast_view(request):
    city_form = CityFormForWeather(request.POST or None)
    context = {'city_form': city_form}
    if request.method == 'POST' and city_form.is_valid():
        city_name = city_form.cleaned_data['city_name']
        weather_service = WeatherService(city_name)
        weather_service.get_weather_and_foreacst()
        context.update({
            'city_name': city_name,
            'weather_data': weather_service.weather_data,
            'forecast_data': weather_service.forecast_data,
        })

    return render(request, "weather_and_forecast.html", context)


@handle_http_errors
def air_pollution_view(request):
    city_form = CityFormForTwoCities(request.POST or None)
    context = {'city_form': city_form}
    if request.method == 'POST' and city_form.is_valid():
        city_name = city_form.cleaned_data['city_name']
        second_city_name = city_form.cleaned_data.get('second_city_name')
        weather_service = WeatherService(city_name)
        weather_service.get_air_pollution()
        air_pollution_data = weather_service.air_pollution_data.to_list()
        context.update({
            'city_name': city_name,
            'air_pollution_data': air_pollution_data,
        })
        if second_city_name:
            second_weather_service = WeatherService(second_city_name)
            second_weather_service.get_air_pollution()
            second_air_pollution_data = second_weather_service.air_pollution_data.to_list()
            comparison_data = weather_service.air_pollution_data.compare_air_quality(
                second_weather_service.air_pollution_data)

            context.update({
                'second_city_name': second_city_name,
                'second_air_pollution_data': second_air_pollution_data,
                'comparison_data': comparison_data,
            })

        return render(request, "air_pollution.html", context)
