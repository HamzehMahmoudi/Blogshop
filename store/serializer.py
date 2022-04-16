from users.serializer import UserSerializer
from django.db.models import fields
from rest_framework import serializers
from . import models


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Order
        fields = (
            "pk",
            "owner",
            "statuse",
            'orderitem_set'
        )


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = ['order', 'qty', 'product', 'price']
