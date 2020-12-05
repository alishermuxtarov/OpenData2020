from rest_framework import serializers

from utils.serializers import ValidatorSerializer
from vehicle.models import VehicleAd


class VehicleAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleAd
        fields = '__all__'


class UrlSerializer(ValidatorSerializer):
    url = serializers.URLField()


class PriceRecommendationsSerializer(serializers.Serializer):
    ads_count = serializers.IntegerField()
    max_price_uzs = serializers.IntegerField()
    min_price_uzs = serializers.IntegerField()
    avg_price_uzs = serializers.IntegerField()
    max_price_usd = serializers.IntegerField()
    min_price_usd = serializers.IntegerField()
    avg_price_usd = serializers.IntegerField()
