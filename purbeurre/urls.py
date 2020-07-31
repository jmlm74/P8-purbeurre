"""purbeurre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from home_app import views as hav
from home_app import errors as err

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home_app/', include('home_app.urls')),
    path('user_app/', include('user_app.urls')),
    path('products_app/', include('products_app.urls')),
    path('', hav.index, name='index'),
    path('autocomplete_search/', hav.autocomplete_search, name='autocomplete_search'),
]

handler400 = 'home_app.errors.handler400'
handler403 = 'home_app.errors.handler403'
handler404 = 'home_app.errors.handler404'
handler500 = 'home_app.errors.handler500'


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
