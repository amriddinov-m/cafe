# Generated by Django 5.1.6 on 2025-03-08 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_remove_product_photo_product_photo_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='created_by',
        ),
    ]
