# Generated by Django 3.0.8 on 2020-07-21 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0007_auto_20200721_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='bookmark',
            field=models.ManyToManyField(blank=True, through='products_app.Bookmark', to='products_app.Product'),
        ),
    ]
