from rest_framework import serializers

from .models import Area, Region


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name']


class RegionSerializer(serializers.ModelSerializer):
    areas = AreaSerializer(many=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'areas']
