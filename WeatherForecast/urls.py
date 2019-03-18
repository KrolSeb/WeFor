from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_main_view),
    path('pl/', views.render_polish_cities_view),
    path('world/', views.render_worldwide_cities_view),
]