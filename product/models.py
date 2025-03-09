from django.db import models

from main.models import BaseModel


class ProductCategory(BaseModel):
    name = models.CharField(verbose_name='Название', max_length=100)
    key = models.CharField(verbose_name='Уникальное название', max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория блюд'
        verbose_name_plural = 'Категории блюд'


class Product(BaseModel):
    category = models.ForeignKey('product.ProductCategory',
                                 verbose_name='Категория',
                                 on_delete=models.CASCADE,
                                 related_name='products')
    name = models.CharField(verbose_name='Название', max_length=255)
    price = models.DecimalField(verbose_name='Стоимость блюда', max_digits=10, decimal_places=2)
    photo_url = models.CharField(verbose_name='Путь к фото', max_length=255, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

