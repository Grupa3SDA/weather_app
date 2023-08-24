from django.shortcuts import render
from weather_app.get_weather import get_weather_data, get_forecast_data, get_air_pollution_data
from weather_app.forms import CityForm


def home_view(request):
    # set variables below as None by default
    city_form = CityForm(request.GET or None)
    city_name = None
    weather_data = None
    forecast_data = None
    air_pollution_data = None
    weather_error_message = None

    if request.GET and city_form.is_valid():
        city = city_form.cleaned_data['city']
        weather_data = get_weather_data(city)
        city_name = city

        if 'error' in weather_data:
            weather_error_message = weather_data['error']

    if weather_data and 'coord' in weather_data:
        latitude = weather_data['coord']['lat']
        longitude = weather_data['coord']['lon']
        forecast_data = get_forecast_data(latitude, longitude)
        air_pollution_data = get_air_pollution_data(latitude, longitude)

    context = {
        'city_form': city_form,
        'city_name': city_name,
        'weather_data': weather_data,
        'forecast_data': forecast_data,
        'air_pollution_data': air_pollution_data,
        'weather_message': weather_error_message,
    }

    return render(request, 'home.html', context)
