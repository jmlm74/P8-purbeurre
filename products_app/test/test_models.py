from django.test import TransactionTestCase
import inspect
from mixer.backend.django import mixer
from products_app.models import Product, Category, Bookmark

from user_app.models import User


class TestUserAppModels(TransactionTestCase):
    """
        Test methods in models
    """

    def setUp(self):
        """"
        Setup method --> initialize datas to test models methods
        """
        super(TestUserAppModels, self).setUpClass()
        mixer.cycle(3).blend(Product, pname=mixer.sequence('prod{0}'),
                             code=mixer.sequence('{0}'),
                             nutriscore_score=25,
                             nutriscore_grade="e",
                             salt=mixer.RANDOM('H', 'M', 'L', 'U'),
                             sugar=mixer.RANDOM('H', 'M', 'L', 'U'),
                             fat=mixer.RANDOM('H', 'M', 'L', 'U'),
                             saturated_fat=mixer.RANDOM('H', 'M', 'L', 'U'),
                             category__cname=mixer.sequence('category{0}'),
                             brand__bname=mixer.sequence('brand{0}'),
                             store__sname=mixer.sequence('store{0}'))
        # add a cat to a product
        prod2 = Product.objects.get(pname='prod2')
        cat1 = Category.objects.get(cname='category1')
        prod2.category.add(cat1)
        prod2.save()
        # for p in Product.objects.all():
        #    print(f"p0 : {p.pname} - {p.category.all()}")

    def tearDown(self):
        """
        Teardown method --> not used here
        """
        pass

    def test_method_nutrient_levels_returns_good_value(self):
        """
        Verify property Product.get_nutrient_levels returns good values
        """
        print(inspect.currentframe().f_code.co_name)
        prod = Product.objects.get(pname='prod1')
        nutrients = prod.get_nutrient_levels
        salt = nutrients['salt'][0]
        self.assertIn(salt, ['H', 'M', 'L', 'U'])

    def test_method_search_product_return_one_product(self):
        """
        Verify method Product.search_product can return only one product 
            if the name is a product_name
        """
        print(inspect.currentframe().f_code.co_name)
        prod = Product.search_product('prod1')
        self.assertEquals(prod.count(), 1)

    def test_method_search_product_return_3_products(self):
        """
        Verify method Product.search_product returns more than one product
            if the name is not a name product bat math as like %name% (here 3 products)
        """
        print(inspect.currentframe().f_code.co_name)
        prods = Product.search_product('prod')
        self.assertEquals(prods.count(), 3)

    def test_method_search_product_return_empty_dict(self):
        """
        Verify method Product.search_product returns empty queryset if no product found
        """
        print(inspect.currentframe().f_code.co_name)
        prods = Product.search_product('toto')
        self.assertEquals(len(prods), 0)

    def test_method_create_bookmark_ok(self):
        """
        Verify method Bookmark.create_bookmark create a bookmark
        """
        print(inspect.currentframe().f_code.co_name)
        user = mixer.blend(User)
        prod1 = Product.objects.get(pname='prod1')
        prod2 = Product.objects.get(pname='prod2')
        Bookmark.create_bookmark(user, prod1.code, prod2.code)
        bookmarks = Bookmark.objects.all()
        self.assertEquals(bookmarks.count(), 1)
