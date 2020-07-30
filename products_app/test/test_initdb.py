from django.test import TestCase, TransactionTestCase
import json
import pathlib
import inspect


from products_app.tasks import insert_product
from products_app.models import Product, Category, Brand, Store


class TestInitdb(TransactionTestCase):
    """
        Test the initdb task --> passed by Celery ! 
    """
    def test_initdb(self):
        """
            Test the init_db with a file instead of request data from openFoodFacts
        """
        print(inspect.currentframe().f_code.co_name)
        fic_json = pathlib.Path(__file__).parent.joinpath("response.json")
        # fic_json = './static/response.json'
        json_data = open(fic_json, 'r')
        text = json_data.read()
        json_data.close()
        result = {}
        result = json.loads(text)
        for prod in result['products']:
            insert_product(prod)
        count_products = Product.objects.all().count()
        # 17 products have been added
        self.assertEquals(count_products, 17)
        count_cat = Category.objects.all().count()
        # 52 categories have been added
        self.assertEquals(count_cat, 52)
        count_brands = Brand.objects.all().count()
        # 4 brands have been added
        self.assertEquals(count_brands, 4)
        count_stores = Store.objects.all().count()
        # 15 stores have been added
        self.assertEquals(count_stores, 15)
