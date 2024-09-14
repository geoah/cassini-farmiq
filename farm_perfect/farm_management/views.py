from django.shortcuts import render, redirect, get_object_or_404
from .models import Plot, Season, SeasonalEvent
from .forms import PlotForm, SeasonForm, SeasonalEventForm

def plot_list(request):
    plots = Plot.objects.all()
    return render(request, 'farm_management/plot_list.html', {'plots': plots})

def plot_create(request):
    if request.method == 'POST':
        form = PlotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plot_list')
    else:
        form = PlotForm()
    return render(request, 'farm_management/plot_form.html', {'form': form})

def plot_detail(request, plot_id):
    plot = get_object_or_404(Plot, pk=plot_id)
    seasons = plot.seasons.all()
    
    # Fetch timeseries data for each season
    for season in seasons:
        season.cloud_timeline = season.fetch_cloud_timeline(season.start_date, season.end_date)
        season.precipitation = season.fetch_precipitation(season.start_date, season.end_date)
        season.methane = season.fetch_methane(season.start_date, season.end_date)
    
    return render(request, 'farm_management/plot_detail.html', {
        'plot': plot,
        'seasons': seasons,
    })

def season_create(request, plot_pk):
    plot = get_object_or_404(Plot, pk=plot_pk)
    if request.method == 'POST':
        form = SeasonForm(request.POST)
        if form.is_valid():
            season = form.save(commit=False)
            season.plot = plot
            season.save()
            return redirect('plot_detail', pk=plot_pk)
    else:
        form = SeasonForm()
    return render(request, 'farm_management/season_form.html', {'form': form, 'plot': plot})

def event_create(request, season_pk):
    season = get_object_or_404(Season, pk=season_pk)
    if request.method == 'POST':
        form = SeasonalEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.season = season
            event.save()
            return redirect('plot_detail', pk=season.plot.pk)
    else:
        form = SeasonalEventForm()
    return render(request, 'farm_management/event_form.html', {'form': form, 'season': season})
