from django import forms
from .models import Plot, Season, SeasonalEvent
from leaflet.forms.widgets import LeafletWidget
from django.db import models

class PlotForm(forms.ModelForm):
    class Meta:
        model = Plot
        fields = ['name', 'location']
        widgets = {
            'location': LeafletWidget(),
        }

class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = ['crop', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SeasonalEventForm(forms.ModelForm):
    class Meta:
        model = SeasonalEvent
        fields = ['event_date', 'event_type', 'description', 'fertilizer_type', 
                  'fertilizer_amount', 'pest_type', 'disease_type', 
                  'irrigation_amount', 'soil_ph', 'harvest_yield']
    class Meta:
        model = SeasonalEvent
        fields = ['event_date', 'event_type', 'description', 'fertilizer_type', 
                  'fertilizer_amount', 'pest_type', 'disease_type', 
                  'irrigation_amount', 'soil_ph', 'harvest_yield']
        
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'fertilizer_type': forms.TextInput(),
            'fertilizer_amount': forms.NumberInput(),
            'pest_type': forms.TextInput(),
            'disease_type': forms.TextInput(),
            'irrigation_amount': forms.NumberInput(),
            'soil_ph': forms.NumberInput(),
            'harvest_yield': forms.NumberInput(),
        }
