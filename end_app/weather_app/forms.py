from django import forms


class CityFormForWeather(forms.Form):
    city_name = forms.CharField(max_length=20)


class CityFormForPollution(forms.Form):
    city_name = forms.CharField(label="Search city", max_length=20)


class CityFormForTwoCities(CityFormForPollution):
    second_city_name = forms.CharField(label='Search another city', max_length=100, required=False)
