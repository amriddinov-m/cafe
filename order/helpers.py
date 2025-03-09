from order.models import Order


def create_order(data) -> dict:
    # Создаем заказ из JSON
    Order.create_from_json(data)
    return {'message': 'Successfully created order'}


def update_order(data) -> dict:
    # Обновляем заказ из JSON
    Order.update_from_json(data)
    return {'message': 'Successfully updated order'}


def delete_order(data) -> dict:
    Order.objects.filter(id=data.get('order_id')).delete()
    return {'message': 'Successfully deleted order'}


def update_status_order(data) -> dict:
    status = data.get('status')
    order = Order.objects.get(id=data.get('order_id'))

    # Обновляем статус заказа
    order.update_status(status)

    return {'message': 'Successfully updated order status'}
