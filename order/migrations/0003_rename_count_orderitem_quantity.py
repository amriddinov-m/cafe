# Generated by Django 5.1.6 on 2025-03-08 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_remove_order_created_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='count',
            new_name='quantity',
        ),
    ]
