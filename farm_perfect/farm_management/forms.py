from django import forms
from .models import Plot, Season, SeasonalEvent
from leaflet.forms.widgets import LeafletWidget

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

class SeasonalEventForm(forms.ModelForm):
    class Meta:
        model = SeasonalEvent
        fields = ['event_date', 'description']
