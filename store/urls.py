from django.db import router
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("orders", views.OrderViewSet)
router.register("orderitems", views.OrderItemViewSet)
urlpatterns = [
    path("", views.add_to_cart, name="add_cart"),
    path("cart", views.cart_view, name="cart"),
    path("delete_from_cart/<int:product_id>",
         views.delete_row, name="delet_from_cart"),
    path("deduct", views.deduct_from_cart, name="deduct-from-cart"),
    path("api/v1/", include(router.urls)),
    path("order", views.order, name="order"),
    path("orders", views.OrderView.as_view(), name="orders"),
    path("print/<int:pk>", views.PrintOrder.as_view(), name="print-order"),
]
