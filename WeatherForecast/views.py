import pytz
import requests

from django.shortcuts import render
from .models import PolishCity, WorldwideCity
from googletrans import Translator

"""
Definition of final values
"""
no_data_constant = 'b/d'
request_values_separator = ','
utc_timezone = pytz.timezone('utc')
translator = Translator()

current_weather_request_url = 'https://api.weatherbit.io/v2.0/current?city={}&lang=pl&key=65887c016c6c46de8d4b61b81d59a960'


""" Render main application view (on start)
:returns: HTML template
"""
def render_main_view(request):
    path_to_view = 'weather/weather_main.html'
    return render(request, path_to_view)


""" Render view containing basic weather data for polish cities 
:returns: context(dictionary with weather data) and HTML template(view)
"""
def render_polish_cities_view(request):
    path_to_view = 'weather/weather_cities_polish.html'
    polish_cities = PolishCity.objects.all().order_by('name')
    weather_data_for_cities = get_actual_basic_weather_data_for_cities(polish_cities)

    context = {'weather_data_for_cities': weather_data_for_cities}
    return render(request, path_to_view, context)


""" Render view containing basic weather data for worldwide cities 
:returns: context(dictionary with weather data) and HTML template(view)
"""
def render_worldwide_cities_view(request):
    path_to_view = 'weather/weather_cities_worldwide.html'
    worldwide_cities = WorldwideCity.objects.all().order_by('name')
    weather_data_for_cities = get_actual_basic_weather_data_for_cities(worldwide_cities)

    context = {'weather_data_for_cities': weather_data_for_cities}
    return render(request, path_to_view, context)


""" Gets data about actual basic weather for cities from API and store it in list of dictionaries
:param cities: multiple city objects from model
:returns: list of dictionaries
"""
def get_actual_basic_weather_data_for_cities(cities):
    weather_data_for_cities = []
    for city in cities:
        json_response = requests.get(current_weather_request_url.format(city.name + request_values_separator + city.country_code)).json()
        city_weather = {
            'city': json_response["data"][0]['city_name'],
            'country_code': json_response["data"][0]['country_code'],
            'description': json_response["data"][0]['weather']['description'],
            'code': json_response["data"][0]['weather']['code'],
            'temperature': json_response["data"][0]['temp'],
        }

        city_weather['place_url'] = city_weather.get('city').replace(' ','-') + '_' + city_weather.get('country_code')
        city_weather['city'] = translator.translate(city_weather.get('city'),src='en',dest='pl').text
        weather_data_for_cities.append(city_weather)

    return weather_data_for_cities

