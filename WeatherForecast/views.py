from django.shortcuts import render

""" Render main application view (on start)
:returns: HTML template
"""
def render_main_view(request):
    path_to_view = 'weather/weather_main.html'
    return render(request, path_to_view)
