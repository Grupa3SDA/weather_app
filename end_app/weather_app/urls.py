from django.urls import path
from . import views

app_name = 'weather_app'

urlpatterns = [
    path('', views.weather_and_forecast_view, name='weather_and_forecast'),
    path('air_pollution/', views.air_pollution_view, name='air_pollution'),
]
