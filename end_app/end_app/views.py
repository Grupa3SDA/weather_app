from django.shortcuts import render
from weather_app.get_weather import get_weather_data
from weather_app.forms import CityForm


def home_view(request):
    city_form = CityForm(request.GET or None)
    city_name = None

    if request.GET and city_form.is_valid():
        city = city_form.cleaned_data['city']
        weather_data = get_weather_data(city)
    else:
        weather_data = None

    context = {
        'city_form': city_form,
        'weather_data': weather_data,
        'city_name': city_name,
    }

    return render(request, 'home.html', context)
