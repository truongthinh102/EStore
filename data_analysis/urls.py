from unicodedata import name
from django.urls import path
from dashboard import views
from data_analysis import views


app_name = 'data_analysis'
urlpatterns = [
    path('series/', views.series, name="series"),
    path('chart/', views.chart, name="chart"),
]
