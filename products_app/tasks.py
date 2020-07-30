from products_app.models import Category, Brand, Store, Product, ProductsWish, Bookmark
from products_app.init import url, categories, params_off, brands
from django.db.utils import IntegrityError
import re

import requests
import unicodedata


def init_db(init=True, *args):
    """
    Fill tables  from Open Food Facts Data
    Args:
        init (bool, optional): Defaults to False.
        if init --> delete datas in all tables and then fill them
                --> add datas in the tables with all the users wishes
        else --> just add users wishes not already added
    """
    if init:
        print('Init tables from OpenFoodFacts data')
        Product.objects.all().delete()
        Category.objects.all().delete()
        Brand.objects.all().delete()
        Store.objects.all().delete()
        Bookmark.objects.all().delete()
        # brands
        params = dict(params_off)
        for brand in brands:
            print(f"loading brand {brand}")
            params['tag_0'] = brand
            params['tagtype_0'] = "brands"
            response = requests.get(url, params=params)
            # print(f"{url} - {params}")
            if (response.status_code) == 200:
                result = response.json()
                for prod in result['products']:
                    insert_product(prod)
            else:
                print(f"Error Get brand - RC = {response.status_code}")

        # categories
        params = dict(params_off)
        for cat in categories:
            print(f"loading category {cat}")
            params['tag_0'] = cat
            # print(f"{url} - {params}")
            response = requests.get(url, params=params)
            if (response.status_code) == 200:
                result = response.json()
                for prod in result['products']:
                    insert_product(prod)
            else:
                print(f"Error Get category - RC = {response.status_code}")

    init_db_wishes(init)

    # Nb product/category
    print("Update nb_prod in Category")
    categories_s = Category.objects.all()
    for cat in categories_s:
        nbr_prod = Product.objects.filter(category__cname=cat.cname).count()
        upd_cat = Category.objects.get(cname=cat.cname)
        upd_cat.nb_prod = nbr_prod
        upd_cat.save()


def init_db_wishes(init):
    """
    add datas from open food facts with products not found and wished by users
    prepare the request ang GET it  then insert the products found into the database
    """
    print("add users wishes")
    if init:
        results = ProductsWish.objects.all()
    else:
        results = ProductsWish.objects.all().filter(indb=False)
    params = dict(params_off)
    prod_found = False
    if len(results) > 0:
        for result in results:
            params['tag_0'] = ""
            params['tag_type_0'] = ""
            params['tag_contains_0'] = ""
            params['search_terms'] = result.pwname
            params['page_size'] = 50
            url_result = requests.get(url, params=params).json()
            for prod in url_result['products']:
                prod_found = True
                insert_product(prod)
            result.indb = True
            result.save()
            if not prod_found:
                print(f"suppression {result.pwname}")
                ProductsWish.objects.filter(pwname=result.pwname).delete()
    return


def insert_product(prod):

    """
    insert the product in argument into the tables
    Args:
        prod : json fields from the request return
    Test if the fields are well filled and return if no
    add product in database :
        1st the product himself
        2nd the categories, stores and brand
    """
    prod_brands = []
    prod_categories = []
    prod_stores = []
    # verify the product's fields are well filled
    if not test_product_complete(prod,
                                 'product_name',
                                 'brands',
                                 'nutriscore_score',
                                 'nutriscore_grade',
                                 'stores',
                                 'categories',
                                 'image_small_url',  # product image
                                 'url',
                                 'code',  # barecode
                                 'generic_name_fr',   # desc
                                 'unique_scans_n',    # nb scans
                                 'nutrient_levels',   # reperes nutritionnels
                                 ):
        return
    # verify that nutriscore is integer
    if not str(prod['nutriscore_score']).isdigit():
        # print("nutriscore_score not an int")
        return
    # verify that nutriscore is integer
    if not str(prod['unique_scans_n']).isdigit():
        # print("nutriscore_score not an int")
        return

    # add product in database
    # do not decode urls (special chars)
    # validate datas are populated
    pname = decod(prod['product_name'])
    code = decod(prod['code'])
    product_url = prod['url']
    nutriscore_score = int(prod["nutriscore_score"])
    nutriscore_grade = prod["nutriscore_grade"]
    photo_url = prod['image_small_url']
    desc = prod['generic_name_fr']
    nb_scans = prod['unique_scans_n']
    try:
        salt = prod['nutrient_levels']['salt'][:1].upper()
    except KeyError:
        salt = "U"
    try:
        sugar = prod['nutrient_levels']['sugars'][:1].upper()
    except KeyError:
        sugar = "U"
    try:
        fat = prod['nutrient_levels']['fat'][:1].upper()
    except KeyError:
        fat = "U"
    try:
        saturated_fat = prod['nutrient_levels']['saturated-fat'][:1].upper()
    except KeyError:
        saturated_fat = "U"
    try:
        new_product = Product.objects.create(pname=pname,
                                             code=code,
                                             product_url=product_url,
                                             photo_url=photo_url,
                                             nutriscore_score=nutriscore_score,
                                             nutriscore_grade=nutriscore_grade,
                                             desc=desc,
                                             nb_scans=nb_scans,
                                             salt=salt,
                                             sugar=sugar,
                                             fat=fat,
                                             saturated_fat=saturated_fat)
        new_product.save()
    except IntegrityError:
        # print(f"doublon {pname}")
        return
    except:
        # print(f"Unexpected Error on {pname} - {sys.exc_info()[0]}")
        return

    # brand, stores and categories
    prod_brands = prod['brands'].split(',')
    prod_categories = prod['categories'].split(',')
    prod_stores = prod['stores'].split(',')
    for prod_brand in prod_brands:
        prod_brand = decod(prod_brand)
        # print(f"brand : {prod_brand}")
        Brand.objects.get_or_create(bname=prod_brand)
        new_brand = Brand.objects.get(bname=prod_brand)
        new_product.brand = new_brand
        new_product.save()
    for prod_category in prod_categories:
        prod_category = decod(prod_category)
        # print(f"Categorie : {prod_category}")
        Category.objects.get_or_create(cname=prod_category)
        new_category = Category.objects.get(cname=prod_category)
        new_product.category.add(new_category)
    for prod_store in prod_stores:
        prod_store = decod(prod_store)
        # print(f"store : {prod_store}")
        Store.objects.get_or_create(sname=prod_store)
        new_store = Store.objects.get(sname=prod_store)
        new_product.store.add(new_store)

    # print('%s : ok' % prod['product_name'])
    return


def test_product_complete(prod, *args):
    """
    Args:
        prod : json fields from the request return
        *args : fields to verifiy in array

    Verify all the fields in *args are OK in the prod

    Returns:
        True --> All the fields are OK
        False a field is not filled
    """
    for arg in args:
        if arg not in prod:
            # print("ERREUR sur %s - %s not found" % (prod['product_name'], arg))
            return False
    return True


def decod(string):
    """suppress bad characters from string --> encode utf-8

    Args:
        string

    Returns:
        String well formed (utf8)
    """
    if len(string) == 0:
        string = "unknown"
    try:
        string = unicode(string, 'utf-8')
    except (TypeError, NameError):
        pass
    string = unicodedata.normalize('NFD', string)
    string = string.encode('ascii', 'ignore')
    string = string.decode("utf-8")
    string = string.strip()
    string = re.sub(r"[^a-zA-Z0-9]+", ' ', string)
    return string.lower()
