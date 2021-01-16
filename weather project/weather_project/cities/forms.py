from django import forms
from .models import Location
import requests
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class CityForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CityForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        self.name = self.cleaned_data['name']
        self.name = self.name.lower()
        city_list = list(self.name)
        city_list[0] = city_list[0].upper()
        self.name = ''.join(city_list)
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=bbf498e04c4fb60d9c5ba7de18b2af08'
        city_weather = requests.get(
            url.format(self.name)).json()  # request the API data and convert the JSON to Python data types

        def check_user():
            a = Location.objects.filter(name=self.name)
            for location in a:
                if location.user.username==self.user.username:
                    raise ValidationError("City already added!")

        if city_weather['cod'] != '404':
            if Location.objects.filter(name=self.name).exists():
                check_user()
            return self.name

        self.name = slugify(self.name)
        city_list = list(self.name)
        city_list[0] = city_list[0].upper()
        self.name = ''.join(city_list)
        city_weather = requests.get(
            url.format(self.name)).json()
        if city_weather['cod'] == '404':
            raise ValidationError("City does not exit. Please retry!")
        elif Location.objects.filter(name=self.name).exists():
            check_user()
        return self.name
