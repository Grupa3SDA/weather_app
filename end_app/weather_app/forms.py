from django import forms


class CityForm(forms.Form):
    city = forms.CharField(label='Enter city name', max_length=20)
