"""
    home_app URL Configuration

"""
from django.urls import path

from user_app import views as uav
from home_app import views as hav


app_name = 'user_app'
urlpatterns = [
    path('', hav.index, name='index'),
    path('user', uav.user_view, name='user'),
    path('user_logout', uav.user_logout, name='ulogout'),
]
