from django.db import models

from main.models import BaseModel


class Order(BaseModel):
    class Status(models.TextChoices):
        pending = 'pending', 'В ожидании'
        ready = 'ready', 'Готово'
        paid = 'paid', 'Оплачено'

    table = models.ForeignKey('main.Table', verbose_name='Номер стола', on_delete=models.CASCADE)
    total_price = models.DecimalField(verbose_name='Общая стоимость заказа', default=0, max_digits=10, decimal_places=2)
    status = models.CharField(verbose_name='Статус', max_length=255, choices=Status.choices, default=Status.pending)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - Table {self.table}"

    def update_status(self, new_status):
        """Обновляет статус заказа"""
        if new_status in self.Status.values:
            self.status = new_status
            self.save()
        else:
            raise ValueError(f"Неверный статус: {new_status}")

    def calculate_total_price(self):
        """Пересчитывает общую стоимость заказа"""
        total = sum(item.product.price * item.quantity for item in self.orderitem_set.all())
        self.total_price = total
        self.save()
        return total

    @classmethod
    def create_from_json(cls, data):
        """Создает заказ из JSON"""
        items = data.get('items', [])
        order = cls.objects.create(table_id=data.get('table_id'))

        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            OrderItem.objects.create(order=order, product_id=product_id, quantity=quantity)

        order.calculate_total_price()
        return order

    @classmethod
    def update_from_json(cls, data):
        """Обновляет заказ из JSON"""
        order = cls.objects.get(id=data["order_id"])
        order.table_id = data.get("table_id", order.table_id)
        order.save()

        # Удаляем старые позиции заказа
        OrderItem.objects.filter(order=order).delete()

        # Добавляем новые позиции
        order_items = [
            OrderItem(order=order, product_id=item["product_id"], quantity=item["quantity"])
            for item in data["items"]
        ]
        OrderItem.objects.bulk_create(order_items)

        # Пересчитываем сумму
        order.calculate_total_price()

        return order

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-id']


class OrderItem(models.Model):
    order = models.ForeignKey('Order',
                              verbose_name='Заказ',
                              on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product',
                                verbose_name='Блюдо',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f"{self.product.name} - {self.order}"
