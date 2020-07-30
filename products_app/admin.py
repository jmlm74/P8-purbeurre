from django.contrib import admin
from products_app import models

# Register your models here.
admin.site.register(models.Brand)
admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.Store)
admin.site.register(models.ProductsWish)
admin.site.register(models.Bookmark)