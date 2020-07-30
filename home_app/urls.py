"""
    home_app URL Configuration

"""
from django.urls import path

from home_app import views as hav


app_name = 'home_app'
urlpatterns = [
    path('', hav.index, name='index'),
    path('index/', hav.index, name='index'),
    path('mentions/', hav.mentions, name='mentions'),
]
