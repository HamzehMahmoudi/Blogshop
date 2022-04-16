from inventory.models import Product
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('inventory', views.ProductViewSet)
urlpatterns = [
    path("", views.Productview.as_view(), name="products"),
    path("api/v1/", views.ProductList.as_view(), name="product_api"),
    path("list", views.product_list, name="product_list"),
    path("list2", views.ProductList2.as_view(), name="product_list2"),
]
