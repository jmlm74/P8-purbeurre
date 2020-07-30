from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView, TemplateView, ListView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
import json
from django.db.utils import IntegrityError
import threading


from products_app.tasks import init_db
from products_app.init import NB_ITEMS_PAGE
from products_app import substitutes as subst
from products_app.models import Product, Bookmark, ProductsWish


def search_view(request):
    """
        Display 1st resul of product search
        depends on search result :
        - Error --> just display the message
        - no product found --> ask to fetch data via openfoodfacts API en rertry the search later
        - more than one product found --> display all the product to choose one and the go to the
            substitute page with this product
        - 1 product found --> just go to the substitute page with the found product
    """
    context = {'title': 'Search'}
    if not request.user.is_authenticated:
        # user not authenticated --> not a 404 but a message !
        context['search_return'] = "4"
        return render(request, 'products_app/search.html', context=context)

    if request.method == 'POST':
        if 'chkcode' in request.POST:
            # product has been chosen in the list
            # put the barecode in session data
            # Get search_substitute
            request.session['code'] = request.POST['chkcode']
            return HttpResponseRedirect(reverse('products_app:search_substitute'))

        if 'yes' not in request.POST:
            # 1st passage
            try:
                context['item'] = request.POST['items_to_search']
            except MultiValueDictKeyError:
                context['item'] = request.POST['search_menu']
            # Search product --> return a queryset (None is an error)
            prod_to_search = Product.search_product(context['item'])
            request.session['item'] = context['item']
            if prod_to_search is None:
                # Error in search --> just display the message
                context['search_return'] = "0"
                return render(request, 'products_app/search.html', context=context)

            if len(prod_to_search) == 0:
                # Nothing found --> ask to fetch from OpenFoodFacts and then try again later
                context['search_return'] = "1"
                return render(request, 'products_app/search.html', context=context)
            elif len(prod_to_search) > 1:
                # More than one product found !!
                # paginator for the products
                page_obj = paginate(prod_to_search, 1)

                context['prods'] = page_obj
                context['search_return'] = "2"
                return render(request, 'products_app/search.html', context=context)
            else:
                # one product found redirect  search_substitute
                prod = prod_to_search.first()
                request.session['code'] = prod.code
                context['search_return'] = "3"
                return HttpResponseRedirect(reverse('products_app:search_substitute'))
        else:
            # no product found --> yes to search in openfoodfacts data
            item = request.session['item']
            try:
                ProductsWish.objects.create(pwname=item)
            except IntegrityError:
                pass
            task = threading.Thread(target=init_db, args=(False, ))
            task.start()
            return HttpResponseRedirect(reverse('home_app:index'))

    elif request.method == 'GET':
        # for the pagination  --> more than one product
        prod_to_search = Product.search_product(request.session['item'])
        # paginator
        page_number = int(request.GET.get('page', 1))
        page_obj = paginate(prod_to_search, page_number)

        context['search_return'] = "2"
        context['prods'] = page_obj
    return render(request, 'products_app/search.html', context=context)


def search_substitute_view(request):
    """
    fonction based view to select a substitute
    the product is in the request

    always with the get method
    Get the product through the barcode (more efficient than the name !)

    render the search_substitute.html template
    """
    context = {}
    if request.method == 'POST':
        pass
    else:
        prod_to_search = Product.objects.get(code=request.session['code'])
        context['chk'] = prod_to_search
        substitutes = subst.search_substitute(prod_to_search)
        # find the barcodes for all the selected product substitutes already bookmarked
        # put the in an array to get the green or red floppy !
        bookmarks = subst.search_bookmarks(prod_to_search.code, request.user.username)
        list_code_bookmarks = []
        for bookmark in bookmarks:
            list_code_bookmarks.append(bookmark.substitute.code)
            # The paginator
        if substitutes is not None:
            page_number = int(request.GET.get('page', 1))
            page_obj = paginate(substitutes, page_number)
            context['substitutes'] = page_obj
            context['list_bookmarks'] = list_code_bookmarks
        context['title'] = "Select Substitute"
    return render(request, "products_app/search_substitute.html", context=context)


@csrf_exempt
def save_bookmark(request):
    """
    Save a bookmark in database.
    called by Ajax but with POST (security reason). The decorator csrf_exempt is to avoid to generate
    a csrf token in the javascript
    args : request
        the products (origin and bookmarks ) are in the request in json format
    returns : OK or error in json format
    """
    if request.method == 'POST':
        request_data = json.loads(request.read().decode('utf-8'))
        user = request.user.username
        prod = str(request_data['subst'])
        subst = str(request_data['prod'])
        try:
            Bookmark.create_bookmark(user, subst, prod)
            data = {'data': 'OK'}
        except:
            data = {'data': 'ERREUR'}
    return JsonResponse(data)


class ProductDetailView(DetailView):
    """
    Detail of a product --> detail view
    The query is in get_object method

    """
    context_object_name = 'product'
    model = Product
    template_name = "products_app/detail_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self):
        return Product.objects.get(code=self.code)
    """
    not used --> to be validated
    def get(self, request, *args, **kwargs):
        # print("get detail_view")
        self.code = request.session['code']
        self.object = self.get_object()
        context = self.get_context_data()
        return self.render_to_response(context=context)
    """
    def post(self, request, *args, **kwargs):
        self.code = request.POST['chkcode']
        self.object = self.get_object()
        context = self.get_context_data()
        context['nutrient_levels'] = self.object.get_nutrient_levels
        context['title'] = 'Product Detail'
        return self.render_to_response(context=context)


@method_decorator(staff_member_required, name='get')
class InitDBView(TemplateView):
    """
    The initDB page
    - get method (to obtain the page)
        - Protected by the class decorator
    - post method if OK --> launch the InitDB
        - The initDB task is launch as a celery task "(delay) method)" : it runs in background
        - Return immediatly to the homepage without waiting the end of InitDB
    """
    template_name = "products_app/initdb.html"
    context_object_name = 'init'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['title'] = 'InitDB'
        return self.render_to_response(context=context)

    @method_decorator(staff_member_required())
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['title'] = 'InitDB'
        task = threading.Thread(target=init_db, args=(True, ))
        task.start()
        return HttpResponseRedirect(reverse('home_app:index'))


class BookmarkListView(ListView):
    """
    ListView for the bookmarks list
    Just a queryset defined and a context for the title
    """
    model = Bookmark
    template_name = "products_app/list_bookmarks.html"
    context_object_name = 'bookmarks'
    ordering = ['product']

    def get_queryset(self):
        queryset = self.model.objects.all().filter(buser=self.request.user).distinct('product')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List Bookmarks'
        return context


def paginate(items, page_number):
    """
    paginator
    the NB_ITEMS_PAGE is defined in the setup.py
    args : items to paginate (queryset in example)
           page number --> in the page request --> send by the caller

    return the part of the items to be displayed (a part of a queryset in example :
        from 12 to 24 for the 2nd page)
    """
    paginator = Paginator(items, NB_ITEMS_PAGE)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj
