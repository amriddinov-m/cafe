from django.urls import path
from rest_framework import routers

from order.api_views import OrderViewSet
from order.views import OrderCreateView, OrderActionView, OrderListView, OrderUpdateView, RevenueView

router = routers.SimpleRouter()

router.register('order', OrderViewSet, basename='order_view_set')

urlpatterns = [
    path('list/', OrderListView.as_view(), name='order-list'),
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('update/<int:pk>/', OrderUpdateView.as_view(), name='order-update'),
    path('revenue/', RevenueView.as_view(), name='order-revenue'),
    path('action/', OrderActionView.as_view(), name='order-action'),
]
