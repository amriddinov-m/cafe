# Generated by Django 5.1.6 on 2025-03-06 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_remove_product_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='photo',
        ),
        migrations.AddField(
            model_name='product',
            name='photo_url',
            field=models.CharField(max_length=255, null=True, verbose_name='Путь к фото'),
        ),
    ]
