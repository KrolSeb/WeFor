from django.forms import ModelForm, TextInput
from .models import FavouriteCity

class CityForm(ModelForm):
    class Meta:
        model = FavouriteCity
        fields = ['name']
        widgets = {'name' : TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Nazwa miasta'})}
