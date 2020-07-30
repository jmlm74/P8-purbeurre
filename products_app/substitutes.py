from products_app.models import Category, Product
import user_app.models as uam


def search_substitute(prod_selected):
    """
    Get the most populated category of the product then return products that are in the same
        category with a nutriscore_score less or equal
        loop in the product categories to find good substitutes : with one or more common categories
        If we have 6 or less substitutes --> return the products to have a good choice !

    args : prod_selected : product

    returns : products in the same category with a better or same nutriscoe (queryset)
    """
    ns = prod_selected.nutriscore_score
    # get the categories --> return a query set
    cats = Category.objects.filter(products__pname=prod_selected.pname).order_by('-nb_prod')
    # get all the products which nutriscore_score less than our product
    prods = Product.objects.filter(nutriscore_score__lte=ns).exclude(pname=prod_selected.pname)
    # loop to filter on the categories until 6 products or less
    passed = 0
    for cptr_cat in range(cats.count()):
        newprods = prods.filter(category__cname=cats[cptr_cat].cname)
        if newprods.count() > 0:
            passed = 1
            prods = newprods
        else:
            break
        if prods.count() <= 12:
            break
    if cptr_cat == 0 and passed == 0:
        return None
    if prods:
        prods = prods.order_by('nutriscore_score', 'nb_scans')
        return prods
    else:
        return None


def search_bookmarks(code, user):
    """
    search bookmarks for a product for a specific user
    args :  code : barcode
            user : user
    returns : bookmarks (queryset)
    """
    connected_user = uam.User.objects.get(username=user)
    prod = Product.objects.get(code=code)
    bookmarks = prod.pbookmarks.filter(buser=connected_user)
    return bookmarks
