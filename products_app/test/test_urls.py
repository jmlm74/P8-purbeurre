from django.test import TestCase
from django.urls import reverse, resolve
import inspect

from products_app.views import (search_view, search_substitute_view, ProductDetailView,
                                save_bookmark, BookmarkListView, InitDBView)


class TestUrls(TestCase):
    def test_url_search_is_ok(self):
        """
            test reverse and resolve for search
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('products_app:search')
        self.assertEquals(path, '/products_app/search')
        self.assertEquals(resolve(path).view_name, 'products_app:search')
        self.assertEquals(resolve(path).func, search_view)

    def test_url_search_substitute_is_ok(self):
        """
            test reverse and resolve for search
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('products_app:search_substitute')
        self.assertEquals(path, '/products_app/search_substitute')
        self.assertEquals(resolve(path).view_name, 'products_app:search_substitute')
        self.assertEquals(resolve(path).func, search_substitute_view)
    
    def test_url_detail_is_ok(self):
        """
            test reverse and resolve for search
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('products_app:detail')
        self.assertEquals(path, '/products_app/detail')
        self.assertEquals(resolve(path).view_name, 'products_app:detail')
        self.assertEquals(resolve(path).func.view_class, ProductDetailView)

    def test_url_save_bookmark_is_ok(self):
        """
            test reverse and resolve for search
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('products_app:save_bookmark')
        self.assertEquals(path, '/products_app/save_bookmark/')
        self.assertEquals(resolve(path).view_name, 'products_app:save_bookmark')
        self.assertEquals(resolve(path).func, save_bookmark)

    def test_url_list_bookmarks_is_ok(self):
        """
            test reverse and resolve for search
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('products_app:list_bookmarks')
        self.assertEquals(path, '/products_app/list_bookmarks/')
        self.assertEquals(resolve(path).view_name, 'products_app:list_bookmarks')
        self.assertEquals(resolve(path).func.view_class, BookmarkListView)

    def test_url_initdb_is_ok(self):
        """
            test reverse and resolve for search
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('products_app:initdb')
        self.assertEquals(path, '/products_app/initdb')
        self.assertEquals(resolve(path).view_name, 'products_app:initdb')
        self.assertEquals(resolve(path).func.view_class, InitDBView)



