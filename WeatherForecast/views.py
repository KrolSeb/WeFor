import pytz
import requests

from django.shortcuts import render
from .models import PolishCity, WorldwideCity
from googletrans import Translator
from datetime import datetime

"""
Definition of final values
"""
no_data_constant = 'b/d'
request_values_separator = ','
utc_timezone = pytz.timezone('utc')
translator = Translator()

current_weather_request_url = 'https://api.weatherbit.io/v2.0/current?city={}&lang=pl&key=65887c016c6c46de8d4b61b81d59a960'

nnw_n_direction_limit = 348.75
n_nne_direction_limit = 11.25
nne_ne_direction_limit = 33.75
ne_ene_direction_limit = 56.25
ene_e_direction_limit = 78.75
e_ese_direction_limit = 101.25
ese_se_direction_limit = 123.75
se_sse_direction_limit = 146.25
sse_s_direction_limit = 168.75
s_ssw_direction_limit = 191.25
ssw_sw_direction_limit = 213.75
sw_wsw_direction_limit = 236.25
wsw_w_direction_limit = 258.75
w_wnw_direction_limit = 281.25
wnw_nw_direction_limit = 303.75
nw_nnw_direction_limit = 326.25


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


""" Render view containing extended weather data for polish city
:param polish_city_details: contains city name and country code values 
:returns: context(dictionary with extended weather data) and HTML template(view)
"""
def render_polish_city_details_view(request, polish_city_details):
    city_data = get_city_data_from_link(polish_city_details)
    weather_data_for_city = get_actual_specific_weather_data_for_city(city_data[0],city_data[1])
    check_if_current_weather_data_is_correct(weather_data_for_city)
    set_readable_current_weather_data(weather_data_for_city)

    context = {'city_weather': weather_data_for_city}
    return render(request, 'weather/weather_city_detail.html', context)

""" Render view containing extended weather data for worldwide city
:param kwargs: contains city name and country code values 
:returns: context(dictionary with extended weather data) and HTML template(view)
"""
def render_worldwide_city_details_view(request, world_city_details):
    city_data = get_city_data_from_link(world_city_details)
    weather_data_for_city = get_actual_specific_weather_data_for_city(city_data[0],city_data[1])
    check_if_current_weather_data_is_correct(weather_data_for_city)
    set_readable_current_weather_data(weather_data_for_city)

    context = {'city_weather': weather_data_for_city}
    return render(request, 'weather/weather_city_detail.html', context)


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


""" Gets data about actual specific weather for city from API and store it in dictionary.
:param city_name: name of city
:param country_code: code of country where city exists
:returns: dictionary
"""
def get_actual_specific_weather_data_for_city(city_name,country_code):
    full_city_data = city_name + request_values_separator + country_code
    json_response = requests.get(current_weather_request_url.format(full_city_data)).json()
    weather_data_for_city = {
        'city': json_response["data"][0]['city_name'],
        'country_code': json_response["data"][0]['country_code'],
        'description': json_response["data"][0]['weather']['description'],
        'code': json_response["data"][0]['weather']['code'],
        'temperature': json_response["data"][0]['temp'],
        'temperature_perceptible': json_response["data"][0]['app_temp'],
        'pressure_above_sea_level': json_response["data"][0]['slp'],
        'timezone': json_response["data"][0]['timezone'],
        'observation_time': json_response["data"][0]['ob_time'],
        'cloudy_level': json_response["data"][0]['clouds'],
        'humidity': json_response["data"][0]['rh'],
        'latitude': json_response["data"][0]['lat'],
        'longitude': json_response["data"][0]['lon'],
        'sunrise': json_response["data"][0]['sunrise'],
        'sunset': json_response["data"][0]['sunset'],
        'wind_direction': json_response["data"][0]['wind_dir'],
        'wind_speed': json_response["data"][0]['wind_spd'],
        'visibility': json_response["data"][0]['vis'],
        'rain_equivalent': json_response["data"][0]['precip'],
    }
    weather_data_for_city['city'] = translator.translate(weather_data_for_city.get('city'),src='en',dest='pl').text

    return weather_data_for_city


""" Splits link(city_name and country_code) to two separate values.
:param input: city name and country code in format "city-name_countrycode"
:returns: two values list
"""
def get_city_data_from_link(city_details):
    city_name = (city_details.split('_')[0]).replace('-',' ')
    country_code = city_details.split('_')[1]
    return [city_name,country_code]


""" Set changed values in actual forecast dictionary (e.g after rounded or convert).
:param weather_data_for_city: dictionary with weather forecast data
"""
def set_readable_current_weather_data(weather_data_for_city):
    weather_data_for_city['latitude'] = round_float_value(weather_data_for_city.get('latitude'))
    weather_data_for_city['longitude'] = round_float_value(weather_data_for_city.get('longitude'))
    weather_data_for_city['observation_time'] = convert_observation_time_to_local(weather_data_for_city.get('timezone'),weather_data_for_city.get('observation_time'))
    weather_data_for_city['sunrise'] = convert_sunrise_time_to_local(weather_data_for_city.get('timezone'),weather_data_for_city.get('sunrise'))
    weather_data_for_city['sunset'] = convert_sunrise_time_to_local(weather_data_for_city.get('timezone'),weather_data_for_city.get('sunset'))
    weather_data_for_city['pressure_above_sea_level'] = round_int_value(weather_data_for_city.get('pressure_above_sea_level'))
    weather_data_for_city['visibility'] = round_int_value(weather_data_for_city.get('visibility'))
    weather_data_for_city['wind_speed'] = round_float_value(weather_data_for_city.get('wind_speed'))
    weather_data_for_city['wind_direction'] = convert_wind_degrees_to_direction_code(weather_data_for_city.get('wind_direction'))
    weather_data_for_city['rain_equivalent'] = round_rain_equivalent(weather_data_for_city.get('rain_equivalent'))
    weather_data_for_city['timezone'] = remove_underscore_from_timezone(weather_data_for_city.get('timezone'))


""" Check values in dictionary data (may be of type None) and corrects it if needed.
:param weather_data_for_city: dictionary with weather forecast data
:returns: dictionary with property values.
"""
def check_if_current_weather_data_is_correct(weather_data_for_city):
    for key in weather_data_for_city:
        if weather_data_for_city[str(key)] is None:
            weather_data_for_city[str(key)] = no_data_constant
    return weather_data_for_city


""" Round value (e.g. wind speed) up to two decimal places.
:param value: string value from dictionary
:returns: string previously rounded as float
"""
def round_float_value(value):
    return str(round(float(value), 2))


""" Round value (e.g. pressure) without a fractional part.
:param value: string value from dictionary
:returns: string previously rounded as float
"""
def round_int_value(value):
    return str(int(value))


""" Converts observation time from UTC timezone to local timezone for country.
:param timezone_name: destination timezone
:param observation_time: time value
:returns: converted time in format HH:MM as string
"""
def convert_observation_time_to_local(timezone_name, observation_time):
    local_timezone = pytz.timezone(timezone_name)
    utc_observation_time = datetime.strptime(observation_time, '%Y-%m-%d %H:%M')
    utc_observation_time = utc_observation_time.replace(tzinfo=utc_timezone)
    local_observation_time = utc_observation_time.astimezone(local_timezone)
    return str(local_observation_time.strftime("%H:%M"))


""" Converts sunrise time from UTC timezone to local timezone for country.
:param timezone_name: destination timezone
:param sunrise_time: time value
:returns: converted time in format HH:MM as string
"""
def convert_sunrise_time_to_local(timezone_name, sunrise_time):
    local_timezone = pytz.timezone(timezone_name)
    utc_sunrise_time = datetime.strptime(str(datetime.now().date()) + " " + sunrise_time, '%Y-%m-%d %H:%M')
    utc_sunrise_time = utc_sunrise_time.replace(tzinfo=utc_timezone)
    local_sunrise_time = utc_sunrise_time.astimezone(local_timezone)
    return str(local_sunrise_time.strftime("%H:%M"))


""" Converts sunset time from UTC timezone to local timezone for country.
:param timezone_name: destination timezone
:param sunset_time: time value
:returns: converted time in format HH:MM as string
"""
def convert_sunset_time_to_local(timezone_name, sunset_time):
    local_timezone = pytz.timezone(timezone_name)
    utc_sunset_time = datetime.strptime(str(datetime.now().date()) + " " + sunset_time, '%Y-%m-%d %H:%M')
    utc_sunset_time = utc_sunset_time.replace(tzinfo=utc_timezone)
    local_sunset_time = utc_sunset_time.astimezone(local_timezone)
    return str(local_sunset_time.strftime("%H:%M"))


""" Converts wind degrees value to wind direction code.
:param wind_degrees_str: wind degrees
:returns: wind direction code as string
"""
def convert_wind_degrees_to_direction_code(wind_degrees_str):
    wind_degrees_number = int(wind_degrees_str)
    if nnw_n_direction_limit <= wind_degrees_number <= n_nne_direction_limit:
        return "N"
    elif n_nne_direction_limit <= wind_degrees_number <= nne_ne_direction_limit:
        return "NNE"
    elif nne_ne_direction_limit <= wind_degrees_number <= ne_ene_direction_limit:
        return "NE"
    elif ne_ene_direction_limit <= wind_degrees_number <= ene_e_direction_limit:
        return "ENE"
    elif ene_e_direction_limit <= wind_degrees_number <= e_ese_direction_limit:
        return "E"
    elif e_ese_direction_limit <= wind_degrees_number <= ese_se_direction_limit:
        return "ESE"
    elif ese_se_direction_limit <= wind_degrees_number <= se_sse_direction_limit:
        return "SE"
    elif se_sse_direction_limit <= wind_degrees_number <= sse_s_direction_limit:
        return "SSE"
    elif sse_s_direction_limit <= wind_degrees_number <= s_ssw_direction_limit:
        return "S"
    elif s_ssw_direction_limit <= wind_degrees_number <= ssw_sw_direction_limit:
        return "SSW"
    elif ssw_sw_direction_limit <= wind_degrees_number <= sw_wsw_direction_limit:
        return "SW"
    elif sw_wsw_direction_limit <= wind_degrees_number <= wsw_w_direction_limit:
        return "WSW"
    elif wsw_w_direction_limit <= wind_degrees_number <= w_wnw_direction_limit:
        return "W"
    elif w_wnw_direction_limit <= wind_degrees_number <= wnw_nw_direction_limit:
        return "WNW"
    elif wnw_nw_direction_limit <= wind_degrees_number <= nw_nnw_direction_limit:
        return "NW"
    elif nw_nnw_direction_limit <= wind_degrees_number <= nnw_n_direction_limit:
        return "NNW"
    else:
        return no_data_constant


""" Check rain equivalent value and round, if it's a number
:param value: rain equivalent
:returns: no data code or rounded rain equivalent value
"""
def round_rain_equivalent(value):
    if value is no_data_constant:
        return no_data_constant
    else:
        return str(round_float_value(value))


""" Removes underscore from timezone value.
:param timezone: timezone converted to local timezone
"""
def remove_underscore_from_timezone(timezone):
    return timezone.replace("_", " ")

