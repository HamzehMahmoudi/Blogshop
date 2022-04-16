from django.views.decorators.csrf import csrf_exempt
from store.models import Order
from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView
from . import models
from rest_framework import generics, permissions, viewsets
from . import serializers
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.views import APIView, Response as drf_response
from rest_framework import status

# Create your views here.


class Productview(ListView):
    model = models.Product
    template_name = "inventory/products.html"
    queryset = models.Product.objects.filter(is_active=True)
    paginate_by = 20


"""
REST VIEW
"""


class ProductList(generics.ListAPIView):
    queryset = models.Product.objects.filter(is_active=True)
    serializer_class = serializers.ProductSerializer


@csrf_exempt
@api_view(["GET", "POST"])
def product_list(request):

    if request.method == "GET":
        qs = models.Product.objects.all()
        serializer = serializers.ProductSerializer(qs, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == "POST":
        serializer = serializers.ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.data, status=400)


class ProductList2(APIView):
    def get(self, request, format=None):
        qs = models.Product.objects.all()
        serializer = serializers.ProductSerializer(qs, many=True)
        return drf_response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return drf_response(serializer.data, status=status.HTTP_201_CREATED)
        return drf_response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
