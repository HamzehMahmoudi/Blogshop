"""djangol1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from blog.views import show_all_posts
from rest_framework.routers import DefaultRouter
from store import views as store_views
from users import views as user_views
from inventory import views as inventory_views


router = DefaultRouter()
router.register('store', store_views.OrderViewSet)
router.register('store/orderitems', store_views.OrderItemViewSet)
router.register('users', user_views.UserViewSet)
router.register('inventory', inventory_views.ProductViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls")),
    path("users/", include("users.urls")),
    path("", show_all_posts, name="home"),
    path("inventory/", include("inventory.urls")),
    path("store/", include("store.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path('api/v1/', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
