from django.test import TestCase
from django.urls import reverse, resolve
import inspect

from home_app.views import index, mentions


class TestUrls(TestCase):
    """
        Test urls for home_app
    """

    def test_index_is_ok(self):
        """
            test reverse and resolve for /
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('index')
        self.assertEquals(path, '/')
        self.assertEquals(resolve(path).view_name, 'index')
        self.assertEquals(resolve(path).func, index)

    def test_homeapp_index_is_ok(self):
        """
            test reverse and resolve for home_app/index/
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('home_app:index')
        self.assertEquals(path, '/home_app/index/')
        self.assertEquals(resolve(path).view_name, 'home_app:index')
        self.assertEquals(resolve(path).func, index)

    def test_mentions_id_ok(self):
        """
            test reverse and resolve for /
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('home_app:mentions')
        self.assertEquals(path, '/home_app/mentions/')
        self.assertEquals(resolve(path).view_name, 'home_app:mentions')
        self.assertEquals(resolve(path).func, mentions)