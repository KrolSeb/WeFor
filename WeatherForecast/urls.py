from django.urls import path
from . import views

urlpatterns = [
    path('', views.render_main_view),
    path('pl/', views.render_polish_cities_view),
    path('world/', views.render_worldwide_cities_view),
    path('pl/<polish_city_details>/', views.render_polish_city_details_view, name='polish_city_details'),
    path('world/city/<world_city_details>/', views.render_worldwide_city_details_view, name='world_city_details'),
    path('extended/', views.render_extended_mode_view)
]