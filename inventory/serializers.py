from os import write
from rest_framework import serializers
from . import models
from rest_framework.renderers import JSONRenderer
import csv


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = (
            "name",
            "price",
            "description",
        )


class FruitSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(allow_null=False, required=True, allow_blank=True)

    def create(self, validated_data):
        with open("fruit.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(validated_data)
        return validated_data

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance
