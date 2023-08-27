from django.shortcuts import render
from .data_services import DataView
from .forms import CityFormForWeather


def weather_all_data(request):
    form = CityFormForWeather()
    context = {'form': form}
    if request.method == 'POST':
        form = CityFormForWeather(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city_name']
            data_view = DataView(city_name)
            context = {
                'form': form,
                'city_name': city_name,
                'weather_data': data_view.weather_data,
                'forecast_data': data_view.forecast_data,
                'air_pollution_data': data_view.air_pollution_data,
                'error_message': data_view.error_message
            }

    return render(request, "weather.html", context)
