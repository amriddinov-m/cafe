import json
from django.utils.timezone import now
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from main.models import Table
from order.helpers import create_order, update_order, delete_order, update_status_order
from order.models import Order, OrderItem
from product.models import ProductCategory, Product


class OrderListView(TemplateView):
    """Вьюшка для получения списка заказов"""
    template_name = 'order/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = (Order.objects.only('id', 'table', 'status', 'total_price')
                             .select_related('table')
                             .prefetch_related('orderitem_set__product'))
        return context


class OrderCreateView(TemplateView):
    """Вьюшка для создания нового заказа"""
    template_name = 'order/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = ProductCategory.objects.only('name', 'key')
        context['products'] = Product.objects.select_related('category').only('name',
                                                                              'price',
                                                                              'category',
                                                                              'photo_url')
        context['tables'] = Table.objects.only('number')
        return context


class OrderUpdateView(TemplateView):
    """Вьюшка для обновления существующего заказа"""
    template_name = 'order/update.html'

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(Order, id=pk)
        context['order'] = order
        context['order_items'] = OrderItem.objects.filter(order=order).select_related("product")
        context['product_categories'] = ProductCategory.objects.only('name', 'key')
        context['products'] = Product.objects.select_related('category').only('name',
                                                                              'price',
                                                                              'category',
                                                                              'photo_url')
        context['tables'] = Table.objects.only('number')
        return context


class OrderActionView(View):
    """Вьюшка для выполнения действий над заказами (удаление, обновление и т. д.)"""

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(OrderActionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Некорректный JSON"}, status=400)

        action = data.get('action')
        actions = {
            'create_order': create_order,
            'update_order': update_order,
            'delete_order': delete_order,
            'update_status_order': update_status_order,
        }

        if action not in actions:
            return JsonResponse({"success": False, "error": "Недопустимое действие"}, status=400)

        try:
            response = actions[action](data)
            return JsonResponse(response, safe=True)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)


class RevenueView(TemplateView):
    """Вьюшка для расчета выручки за текущий день"""
    template_name = "order/revenue.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = now().date()

        total_revenue = Order.objects.filter(
            status=Order.Status.paid,
            created_at__date=today
        ).aggregate(total=Sum("total_price"))["total"] or 0

        context["total_revenue"] = total_revenue
        return context
