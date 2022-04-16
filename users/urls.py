from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from . import views
router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
app_name = 'users'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path(
        'profile/edit/',
        views.EditUserProfile.as_view(),
        name='edit-profile'
    ),
    path('api/v1/', include(router.urls))

]
