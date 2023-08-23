from django.shortcuts import render
from weather_app.get_weather import get_weather_data
from weather_app.forms import CityForm


def home_view(request):
    city_form = CityForm(request.GET or None)
    city_name = None  # set city_name to None by default
    weather_data = None
    error_message = None

    if request.GET and city_form.is_valid():
        city = city_form.cleaned_data['city']  # changing variable with the data from the cityform form
        weather_data = get_weather_data(city)
        city_name = city

        if 'error' in weather_data:
            error_message = weather_data['error']

    context = {
        'city_form': city_form,
        'weather_data': weather_data,
        'city_name': city_name,
        'error_message': error_message,
    }

    return render(request, 'home.html', context)
