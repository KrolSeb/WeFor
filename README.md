<h1 align="center"> WeFor - Weather Forecast </h1>
<p align="center">
    <img alt="HG" title="WeFor Logo" src="https://raw.githubusercontent.com/KrolSeb/WeFor/master/WeatherForecast/static/img/extended.png" width="200" height="200">
</p>
<h4 align="center">
  Weather forecast web application created with Python, Django and PostgreSQL database.
</h4>



## Table of contents

- [General info](#general-info)
- [Screenshots](#screenshots)
- [Technologies](#technologies)
- [Demo](#demo)
- [Features](#features)
- [Status](#status)
- [Inspiration](#inspiration)
- [Contact](#contact)

## General info

The project was implemented as a part of classes called programming in Python at the university. 

I wanted to learn the basics of programming web applications, so I used the Django framework. In addition, I could use the knowledge and skills acquired during the classes.

## Technologies

- Django 2.2.1
- Python 3.7.3
- PostgreSQL 11
- The full list of dependencies are listed in [requirements.txt](https://github.com/KrolSeb/WeFor/blob/master/requirements.txt)

## Demo

Here is a working live demo: **[wefor.herokuapp.com](http://wefor.herokuapp.com)**.

## Features

List of features ready:

- getting weather data from [Weatherbit.io](https://www.weatherbit.io/) API
- storing cities and country codes in database
- showing actual weather conditions for the sample polish and worldwide cities
- searching sixteen days forecast for city entered by the user 
- formatting retrieved data to user-friendly format (eg. converting wind direction values to codes, rounding of fractional number parts, converting sunset and sunrise times from UTC to local timezones).

## Status

Project is **finished** and **no longer continue**, because **free version of API** don't meet my expectations (a small number of weather forecast types, low number of API calls per day for user)

But in **future** I want to create more complex weather app, using another API, in a different programming language (JS or Java) and framework. Perhaps I will use the front-end of this project and improve it eg. by adding new animations. 

## Inspiration

Thanks to [@vchuhunova](https://github.com/vchuhunova) for cooperation on a project, design and creation of application main logo.

This application is inspired by YouTube video: [Creating a Weather App in Django Using Python Requests](https://www.youtube.com/watch?v=v7xjdXWZafY). Thanks to [@prettyprinted](https://github.com/prettyprinted) for sharing this video, it helps me to start writing my application.

## Contact

Created by [@KrolSeb](https://krolseb.github.io/blog/) - please feel free to contact me if you need any further information.
