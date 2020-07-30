from django.test import Client, TransactionTestCase
from django.urls import reverse
import inspect
import json
from mixer.backend.django import mixer

from user_app.models import User
from products_app.models import Product, Category


class TestViewsNoUser(TransactionTestCase):
    """
    Test search view with no user connected
    """
    def test_view_search_no_auth_user_return_errorpage(self):
        """
        Verify the search method returns error page if no user connected
        """
        print(inspect.currentframe().f_code.co_name)
        client = Client()
        response = client.get(reverse("products_app:search"))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context.get('search_return'), '4')
        # the template used add '.html' at the end and suppress the '/' at the beginning
        url_search = (reverse('products_app:search') + '.html')[1:]
        self.assertTemplateUsed(response, url_search)
        self.assertContains(response, '<h2>Erreur ! Vous devez être authentifié pour effectuer une recherche ! </h2>')


class TestViewSearch(TransactionTestCase):
    """
    Test search view with user connected (view function)
    """

    def setUp(self):
        """
        setUp --> called before each test in the class
        It will be almost the same for all the views tests
        """
        super(TestViewSearch, self).setUpClass()
        # create 3 products
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
        self.search_url = reverse("products_app:search")
        # init test client
        self.client = Client()
        # create a user and connect with this user
        user = User.objects.create(username='foobar')
        user.set_password('foobar')
        user.save()
        self.user = user
        self.client.login(username='foobar', password='foobar')

    def test_view_search_with_1_product_redirect_search_substitute(self):
        """
        Verify if only 1 file found --> search_substitute view directly
        """
        print(inspect.currentframe().f_code.co_name)
        response = self.client.post(self.search_url, {'items_to_search': "prod1", })
        # valid redirect and redirection
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('products_app:search_substitute'))

    def test_view_search_with_more_than_1_product_propose_substitutes(self):
        """
        Verify if more than one product found --> let choose one product in a list
        """
        print(inspect.currentframe().f_code.co_name)
        response = self.client.post(self.search_url, {'items_to_search': "prod", })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context.get('search_return'), '2')
        # the template used add '.html' at the end and suppress the '/' at the beginning
        url_search = (reverse('products_app:search') + '.html')[1:]
        self.assertTemplateUsed(response, url_search)
        self.assertEquals(response.status_code, 200)

    def test_view_search_with_no_product_found(self):
        """
        Verify if no product found --> Error message
        """
        print(inspect.currentframe().f_code.co_name)
        data = {'item': 'prod4', 'name': 'yes', 'search_menu': 'prod4'}
        response = self.client.post(reverse("products_app:search"), data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context.get('search_return'), '1')
        # the template used add '.html' at the end and suppress the '/' at the beginning
        url_search = (reverse('products_app:search') + '.html')[1:]
        self.assertTemplateUsed(response, url_search)
        self.assertContains(response, '<h3>Erreur lors de la recherche ==> Aucun produit trouvé !</h3>')


class TestViewSearchSubstitute(TransactionTestCase):
    """
    test search_substitute view (function)
    """
    def setUp(self):
        super(TestViewSearchSubstitute, self).setUpClass()
        # create 4 products
        mixer.cycle(4).blend(Product, pname=mixer.sequence('prod{0}'),
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
        # the prod3 will not have any substitute
        prod3 = Product.objects.get(pname='prod3')
        prod3.nutriscore_score = 24
        prod3.save()
        # nb_cat by product --> for the substiture research
        categories_s = Category.objects.all()
        for cat in categories_s:
            nbr_prod = Product.objects.filter(category__cname=cat.cname).count()
            upd_cat = Category.objects.get(cname=cat.cname)
            upd_cat.nb_prod = nbr_prod
            upd_cat.save()
        # init test client
        self.client = Client()
        # create a user and connect with this user
        user = User.objects.create(username='foobar')
        user.set_password('foobar')
        user.save()
        self.user = user
        self.client.login(username='foobar', password='foobar')

    def test_view_search_sustitute_got_product(self):
        """
        Verify search_substitue return at least 1 product and display it
        """
        print(inspect.currentframe().f_code.co_name)
        session = self.client.session
        session['code'] = '2'
        session.save()
        response = self.client.get(reverse("products_app:search_substitute"))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'class="fa fa-save" aria-hidden="true"></i>')
        url_search = (reverse('products_app:search_substitute') + '.html')[1:]
        self.assertTemplateUsed(response, url_search)

    def test_view_search_sustitute_got_no_product(self):
        """
        Verify if no substitute found --> message no substitute
        """
        print(inspect.currentframe().f_code.co_name)
        session = self.client.session
        session['code'] = '3'
        session.save()
        response = self.client.get(reverse("products_app:search_substitute"))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, '<h5>Aucun substitut !!!</h5>')
        url_search = (reverse('products_app:search_substitute') + '.html')[1:]
        self.assertTemplateUsed(response, url_search)


class TestViewSaveBookmark(TransactionTestCase):
    """
    Test save bookmark view (Ajax)
    """
    def setUp(self):
        super(TestViewSaveBookmark, self).setUpClass()
        # create 2 products
        mixer.cycle(2).blend(Product, pname=mixer.sequence('prod{0}'),
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
        # test client
        self.client = Client()
        # user creation
        user = User.objects.create(username='foobar')
        user.set_password('foobar')
        user.save()
        self.user = user
        self.client.login(username='foobar', password='foobar')

    def test_view_save_bookmark_OK(self):
        """
        Verify the save bookmark returns OK if OK !!!!
        """
        print(inspect.currentframe().f_code.co_name)
        json_data = json.dumps({'subst': '1', 'prod': '0'})
        response = self.client.post(reverse('products_app:save_bookmark'),
                                    json_data,
                                    content_type="application/json")
        response_data = response.json()
        self.assertEquals(response_data['data'], 'OK')
        self.assertEquals(response.status_code, 200)

    def test_view_save_bookmark_KO(self):
        """
        Verify the save_bookmark returns ERREUR if Error ! (here : non existent product)
        """
        print(inspect.currentframe().f_code.co_name)
        # subst does not exists
        json_data = json.dumps({'subst': '5', 'prod': '0'})
        response = self.client.post(reverse('products_app:save_bookmark'),
                                    json_data,
                                    content_type="application/json")
        response_data = response.json()
        self.assertEquals(response_data['data'], 'ERREUR')
        self.assertEquals(response.status_code, 200)


class TestViewProductDetail(TransactionTestCase):
    """
    Test the product detail view (DetailView)
    """
    def setUp(self):
        super(TestViewProductDetail, self).setUpClass()
        # create 2 products
        mixer.cycle(2).blend(Product, pname=mixer.sequence('prod{0}'),
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
        self.client = Client()

    def test_view_product_Detail_View(self):
        """
        Test the view is OK
        """
        print(inspect.currentframe().f_code.co_name)
        response = self.client.post(reverse('products_app:detail'), {'chkcode': "1", })
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, '<h5 class="text-center"><strong>Repères nutritionels</strong></h5>')
        self.assertTemplateUsed(response, 'products_app/detail_view.html')


class TestInitDBView(TransactionTestCase):
    """
    Test the initDB view (TemplateView)
    """
    def setUp(self):
        super(TestInitDBView, self).setUpClass()
        self.client = Client()
        user = User.objects.create(username='foobar')
        user.set_password('foobar')
        user.is_staff = True
        user.save()
        self.user = user
        self.client.login(username='foobar', password='foobar')

    def test_view_init_DB_view_get(self):
        """
        Test the view is OK
        """
        print(inspect.currentframe().f_code.co_name)
        session = self.client.session
        session.save()
        response = self.client.get(reverse('products_app:initdb'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Attention : Cette opération va effacer <strong>TOUTES')
        url_search = (reverse('products_app:initdb') + '.html')[1:]
        self.assertTemplateUsed(response, url_search)


class TestBookmarkListView(TransactionTestCase):
    """
    Test Bookmark list view (ListView)
    """
    def setUp(self):
        super(TestBookmarkListView, self).setUpClass()
        # create 4 users
        mixer.cycle(4).blend(Product, pname=mixer.sequence('prod{0}'),
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
        # the prod3 will not have any substitute
        prod3 = Product.objects.get(pname='prod3')
        prod3.nutriscore_score = 24
        prod3.save()
        # nb_cat by product --> for the substiture research
        categories_s = Category.objects.all()
        for cat in categories_s:
            nbr_prod = Product.objects.filter(category__cname=cat.cname).count()
            upd_cat = Category.objects.get(cname=cat.cname)
            upd_cat.nb_prod = nbr_prod
            upd_cat.save()
        self.client = Client()
        # self.factory = RequestFactory()
        user = User.objects.create(username='foobar')
        user.set_password('foobar')
        user.save()
        self.user = user
        self.client.login(username='foobar', password='foobar')

    def test_view_bookmark_list_view_1ormore_bookmark(self):
        """
        verifiy the view with one or more bookmark
        """
        print(inspect.currentframe().f_code.co_name)
        # create bookmark
        json_data = json.dumps({'subst': '1', 'prod': '0'})
        response = self.client.post(reverse('products_app:save_bookmark'),
                                    json_data,
                                    content_type="application/json")
        response = self.client.get(reverse('products_app:list_bookmarks'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, '<div class="col-6 text-center border border-dark">PRODUIT(S)</div>')
        self.assertTemplateUsed(response, 'products_app/list_bookmarks.html')

    def test_view_bookmark_list_view_no_bookmark(self):
        """
        Verify the view if no bookmark for the user --> display message
        """
        print(inspect.currentframe().f_code.co_name)
        response = self.client.get(reverse('products_app:list_bookmarks'))
        self.assertContains(response, '<h5>Aucun Bookmark !!!</h5>')
        self.assertTemplateUsed(response, 'products_app/list_bookmarks.html')
