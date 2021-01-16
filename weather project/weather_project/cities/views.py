from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .forms import CityForm
from .models import Location
import requests
from braces.views import SelectRelatedMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.

class CreateCityView(LoginRequiredMixin, generic.CreateView):
    model = Location
    form_class = CityForm
    success_url = reverse_lazy("cities:all")

    def get_form_kwargs(self):
        kwargs = super(CreateCityView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class LocationList(generic.ListView, LoginRequiredMixin):
    model = Location

    def get_queryset(self):
        self.location_user = self.model.objects.filter(user=self.request.user)
        return self.location_user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["location_user"] = self.location_user
        return context


class LocationDetailView(generic.DetailView, LoginRequiredMixin, SelectRelatedMixin):
    model = Location
    select_related = ("user",)
    template_name = 'cities/location_detail.html'

    def get_object(self, *args, **kwargs):
        self.city = get_object_or_404(Location, name=self.kwargs['name'], user=self.request.user)
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=bbf498e04c4fb60d9c5ba7de18b2af08'
        city_weather = requests.get(
            url.format(self.city)).json()  # request the API data and convert the JSON to Python data types
        self.temp = int(city_weather['main']['temp'])
        self.feels_like = int(city_weather['main']['feels_like'])
        self.humidity = int(city_weather['main']['humidity'])
        self.wind = int(city_weather['wind']['speed'])
        self.temp_min = int(city_weather['main']['temp_min'])
        self.temp_max = int(city_weather['main']['temp_max'])
        self.weather_condition=str(city_weather['weather'][0]['main'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['temp'] = self.temp
        context['city'] = self.city
        context['feels_like'] = self.feels_like
        context['humidity'] = self.humidity
        context['wind'] = self.wind
        context['temp_min'] = self.temp_min
        context['temp_max'] = self.temp_max
        context['location'] = self.city
        context['weather_condition'] = self.weather_condition
        context['wind_miles'] = 0.62*self.wind
        return context


class LocationDeleteView(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = Location
    select_related = ("user",)
    success_url = reverse_lazy("cities:all")
    template_name = 'cities/location_confirm_delete.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "City Deleted")
        return super().delete(*args, **kwargs)
