from django import forms


class CityFormForWeather(forms.Form):
    city_name = forms.CharField(label="Search city", max_length=20)