"""
    home_app URL Configuration

"""
from django.urls import path

from products_app import views as pav
from home_app import views as hav


app_name = 'products_app'
urlpatterns = [
    path('', hav.index, name='index'),
    path('search', pav.search_view, name='search'),
    path('search_substitute', pav.search_substitute_view, name='search_substitute'),
    path('detail', pav.ProductDetailView.as_view(), name='detail'),
    path('save_bookmark/', pav.save_bookmark, name='save_bookmark'),
    path('list_bookmarks/', pav.BookmarkListView.as_view(), name='list_bookmarks'),
    path('initdb', pav.InitDBView.as_view(), name='initdb'),
]
