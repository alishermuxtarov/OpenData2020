from rest_framework import serializers

from vehicle.models import Brand


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']


class BrandSerializer(serializers.ModelSerializer):
    models = ModelSerializer(many=True)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'models']


class ReferenceSerializer(serializers.Serializer):
    brands = BrandSerializer(many=True)
