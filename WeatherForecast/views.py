import pytz
import requests

from django.shortcuts import render
from .models import PolishCity,WorldwideCity,FavouriteCity
from .forms import CityForm
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
two_days_weather_request_url = 'https://api.weatherbit.io/v2.0/forecast/3hourly?city={}&lang=pl&days=2&key=65887c016c6c46de8d4b61b81d59a960'
sixteen_days_weather_request_url = 'https://api.weatherbit.io/v2.0/forecast/daily?city={}&lang=pl&key=65887c016c6c46de8d4b61b81d59a960'

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


""" Render view containing actual weather data and other forecast data for city
:returns: context(1 dictionary: actual weather conditions and 2 lists of dictionaries: two days and sixteen days forecast) and HTML template(view)
"""
def render_extended_mode_view(request):
    form = CityForm(request.POST or None)

    actual_weather_data_for_city = {}
    two_days_forecast_data_for_city = []
    sixteen_days_forecast_data_for_city = []

    city_name = check_if_post_method(request,form)
    if city_name != '':
        city_object = find_city_object(city_name)
        actual_weather_data_for_city = get_current_weather_data(city_object)
        two_days_forecast_data_for_city = get_two_days_forecast_data(city_object)
        sixteen_days_forecast_data_for_city = get_sixteen_days_forecast_data(city_object)

    path_to_view = 'weather/weather_cities_extended.html'
    context = {'actual_weather_for_city': actual_weather_data_for_city,'two_days_forecast_for_city':two_days_forecast_data_for_city,'sixteen_days_forecast_for_city':sixteen_days_forecast_data_for_city,'form': form}
    return render(request,path_to_view,context)


""" Main function used to return list of dictionaries with sixteen days forecast data
:param city_object: contains city name and country code values 
:returns: list of dictionaries
"""
def get_sixteen_days_forecast_data(city_object):
    sixteen_days_forecast_data = get_sixteen_days_weather_data_for_city(city_object.name, city_object.country_code)
    convert_dates_to_readable_format(sixteen_days_forecast_data)
    return sixteen_days_forecast_data

""" Gets data about sixteen days forecast for city from API and store it in list of dictionaries
:param city_name: name of city
:param country_code: code of country where city exists
:returns: list of dictionaries
"""
def get_sixteen_days_weather_data_for_city(city_name, country_code):
    full_city_data = city_name + request_values_separator + country_code
    json_response = requests.get(sixteen_days_weather_request_url.format(full_city_data)).json()

    sixteen_days_weather_data_for_city = []
    for position in json_response['data']:
        one_day_forecast_data = {
            'code': position['weather']['code'],
            'description': position['weather']['description'],
            'temperature': position['temp'],
            'chance_of_rain': position['pop'],
            'date': position['datetime']
        }
        sixteen_days_weather_data_for_city.append(one_day_forecast_data)

    return sixteen_days_weather_data_for_city

""" Set new date format for dictionary in list of dictionaries
:param sixteen_days_forecast_data: list of dictionaries with weather forecast
"""
def convert_dates_to_readable_format(sixteen_days_forecast_data):
    for one_day_data in sixteen_days_forecast_data:
        one_day_data['date'] = convert_date_to_readable_format(one_day_data.get('date'))


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
Functions used to get two days weather forecast data
"""
""" Main function used to return list of dictionaries with two days forecast data
:param city_object: contains city name and country code values 
:returns: list of dictionaries with property values
"""
def get_two_days_forecast_data(city_object):
    two_days_forecast_data = get_two_days_weather_data_for_city(city_object.name, city_object.country_code)
    corrected_two_days_forecast_data = check_if_two_days_forecast_data_is_correct(two_days_forecast_data)
    set_readable_two_days_forecast_data(corrected_two_days_forecast_data)
    return corrected_two_days_forecast_data

""" Gets data about two days forecast for city from API and store it in list of dictionaries
:param city_name: name of city
:param country_code: code of country where city exists
:returns: list of dictionaries
"""
def get_two_days_weather_data_for_city(city_name, country_code):
    full_city_data = city_name + request_values_separator + country_code
    json_response = requests.get(two_days_weather_request_url.format(full_city_data)).json()

    two_days_weather_data_for_city = []
    for position in json_response['data']:
        three_hour_forecast_data = {
            'code': position['weather']['code'],
            'description': position['weather']['description'],
            'datetime': position['datetime'],
            'wind_gust_speed': position['wind_gust_spd'],
            'wind_direction': position['wind_dir'],
            'temperature': position['temp'],
            'chance_of_rain': position['pop'],
            'cloudy_level': position['clouds'],
            'pressure_above_sea_level': position['slp']
        }
        date_and_time_values = get_time_and_date_from_datetime(three_hour_forecast_data.get('datetime'))
        three_hour_forecast_data['time'] = date_and_time_values[0]
        three_hour_forecast_data['date'] = date_and_time_values[1]
        two_days_weather_data_for_city.append(three_hour_forecast_data)

    return two_days_weather_data_for_city

""" Splits datetime field to time and date
:param date_time: datetime value
:returns: list with data from API
"""
def get_time_and_date_from_datetime(date_time):
    date = date_time.split(':')[0]
    time = date_time.split(':')[1] + ':00'
    return [time,date]

""" Check values in list of dictionaries data (may be of type None) and corrects it if needed.
:param two_days_forecast_data: list of dictionaries with weather forecast data
:returns: list of dictionaries with property values
"""
def check_if_two_days_forecast_data_is_correct(two_days_forecast_data):
    for single_hour_data in two_days_forecast_data:
        for key in single_hour_data:
            if single_hour_data[str(key)] is None:
                single_hour_data[str(key)] = no_data_constant

    return two_days_forecast_data

""" Converts date to format "day.month"
:param input_date: string value of date
:returns: string value of date in format "day.month"
"""
def convert_date_to_readable_format(input_date):
    return str(datetime.strptime(input_date, '%Y-%m-%d').strftime('%d.%m'))

""" Set changed values for dictionary in list of dictionaries (e.g after rounded or convert)
:param two_days_forecast_data: list of dictionaries with weather forecast data
"""
def set_readable_two_days_forecast_data(two_days_forecast_data):
    for single_hour_data in two_days_forecast_data:
        single_hour_data['date'] = convert_date_to_readable_format(single_hour_data.get('date'))
        single_hour_data['pressure_above_sea_level'] = round_int_value(single_hour_data.get('pressure_above_sea_level'))
        single_hour_data['wind_gust_speed'] = round_int_value(single_hour_data.get('wind_gust_speed'))
        single_hour_data['wind_direction'] = convert_wind_degrees_to_direction_code(single_hour_data.get('wind_direction'))


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
Functions used to get city object from input form - extended forecast
"""

""" Check if the form is used
:param form: form object
:returns: city name or empty string(if form is not used)
"""
def check_if_post_method(request,form):
    if request.method == 'POST':
        if form.is_valid():
            return request.POST['name']
    else:
        return ''

""" Check if city object exists in model
:param city_name: name of city
:returns: city_object or nothing
"""
def find_city_object(city_name):
    for city_object in FavouriteCity.objects.all():
        if city_name.lower() == city_object.name:
            return city_object


"""
Functions used to get actual weather in:
extended weather view for city
specific weather view for city
basic weather view for cities
"""

""" Main function used to return list of dictionaries with actual weather data
:param city_object: contains city name and country code values 
:returns: list of dictionaries
"""
def get_current_weather_data(city_object):
    actual_weather_data_for_city = get_actual_specific_weather_data_for_city(city_object.name, city_object.country_code)
    corrected_actual_weather_data_for_city = check_if_current_weather_data_is_correct(actual_weather_data_for_city)
    set_readable_current_weather_data(corrected_actual_weather_data_for_city)

    return corrected_actual_weather_data_for_city


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

