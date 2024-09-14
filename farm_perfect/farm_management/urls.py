from django.urls import path
from . import views

urlpatterns = [
    path('plots/', views.plot_list, name='plot_list'),
    path('plots/add/', views.plot_create, name='plot_create'),
    path('plots/<int:pk>/', views.plot_detail, name='plot_detail'),
    path('plots/<int:plot_pk>/seasons/add/', views.season_create, name='season_create'),
    path('seasons/<int:season_pk>/events/add/', views.event_create, name='event_create'),
]
