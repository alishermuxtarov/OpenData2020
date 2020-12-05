from rest_framework import serializers

from utils.serializers import ValidatorSerializer
from vehicle.enums import TransmissionType, VehicleCondition
from vehicle.models import VehicleAd


class VehicleAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleAd
        fields = '__all__'


class UrlSerializer(ValidatorSerializer):
    url = serializers.URLField()


class VehicleParametersValidator(ValidatorSerializer):
    model_name = serializers.CharField(required=False)
    model_id = serializers.IntegerField(required=False)
    manufactured_year = serializers.IntegerField(allow_null=True, required=False)
    transmission_type = serializers.ChoiceField(choices=TransmissionType.choices, required=False, allow_null=True, allow_blank=True)
    condition = serializers.ChoiceField(choices=VehicleCondition.choices, required=False, allow_null=True, allow_blank=True)
    driven_km = serializers.IntegerField(allow_null=True, required=False)


class PriceRecommendationsSerializer(serializers.Serializer):
    ads_count = serializers.IntegerField()
    max_price_uzs = serializers.IntegerField()
    min_price_uzs = serializers.IntegerField()
    avg_price_uzs = serializers.IntegerField()
    max_price_usd = serializers.IntegerField()
    min_price_usd = serializers.IntegerField()
    avg_price_usd = serializers.IntegerField()


class AvgPriceByManufacturedYearSerializer(serializers.Serializer):
    manufactured_year = serializers.IntegerField()
    avg_price_usd = serializers.IntegerField()
    avg_price_uzs = serializers.IntegerField()


class AvgPriceByDrivenKmSerializer(serializers.Serializer):
    driven_km = serializers.IntegerField()
    avg_price_usd = serializers.IntegerField()
    avg_price_uzs = serializers.IntegerField()


class RecommendationSerializer(serializers.Serializer):
    prices = PriceRecommendationsSerializer().data
    similar_ads = VehicleAdSerializer(many=True).data
    stats_by_manufactured_year = AvgPriceByManufacturedYearSerializer(many=True)
    stats_by_driven_km = AvgPriceByDrivenKmSerializer(many=True).data
