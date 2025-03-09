from rest_framework import serializers

from order.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def get_product(self, obj):
        return obj.product.name


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    table = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    order_items = OrderItemSerializer(many=True, source='orderitem_set')

    class Meta:
        model = Order
        fields = ['id', 'status', 'total_price', 'table', 'order_items', 'created_at', 'updated_at', ]

    def get_total_price(self, obj):
        return f'${obj.total_price}'

    def get_status(self, obj):
        return obj.get_status_display()

    def get_table(self, obj):
        return f'#{obj.table.number}'
