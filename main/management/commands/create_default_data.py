import os

from django.core.management import BaseCommand

from cafe import settings
from main.models import Table
from product.models import Product, ProductCategory


class Command(BaseCommand):
    help = "Создает тестовые данные для использования системы"

    def handle(self, *args, **kwargs):

        categories_data = [
            {"name": "Горячее", "key": "main"},
            {"name": "Напитки", "key": "drinks"},
            {"name": "Десерты", "key": "desserts"},
        ]

        products_data = [
            {"name": "Бургер", "price": 9.99, "category_key": "main",
             "photo_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300"},
            {"name": "Чизбургер", "price": 5.99, "category_key": "main",
             "photo_url": "https://images.unsplash.com/photo-1508737027454-e6454ef45afd?w=300"},
            {"name": "Пицца", "price": 12.99, "category_key": "main",
             "photo_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=300"},
            {"name": "Салат", "price": 7.99, "category_key": "main",
             "photo_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=300"},
            {"name": "Паста", "price": 11.99, "category_key": "main",
             "photo_url": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=300"},
            {"name": "Кофе", "price": 3.99, "category_key": "drinks",
             "photo_url": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=300"},
            {"name": "Смузи", "price": 4.99, "category_key": "drinks",
             "photo_url": "https://images.unsplash.com/photo-1505252585461-04db1eb84625?w=300"},
            {"name": "Мороженное", "price": 6.99, "category_key": "desserts",
             "photo_url": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=300"},
            {"name": "Мороженное", "price": 6.99, "category_key": "desserts",
             "photo_url": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=300"},
        ]

        # Создаём категории
        category_map = {}
        for cat in categories_data:
            category, created = ProductCategory.objects.get_or_create(name=cat["name"], key=cat["key"])
            category_map[cat["key"]] = category

        # Создаём продукты
        for item in products_data:
            category = category_map.get(item["category_key"])  # Получаем категорию по key
            if not Product.objects.filter(name=item["name"]).exists():
                Product.objects.create(
                    name=item["name"],
                    price=item["price"],
                    photo_url=item["photo_url"],
                    category=category
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Добавлен продукт: {item["name"]} в категорию {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Продукт "{item["name"]}" уже существует'))

        # Создаём 10 столов
        for i in range(1, 11):
            table, created = Table.objects.get_or_create(number=i)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан стол №{i}'))
            else:
                self.stdout.write(self.style.WARNING(f'Стол №{i} уже существует'))

        self.stdout.write(self.style.SUCCESS('Все данные загружены!'))
