from django.http import Http404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from vehicle.management.commands.aggregate import Command
from vehicle.models import VehicleAd, Brand
from vehicle.serlializers.reference import ReferenceSerializer
from vehicle.serlializers.vehicle import UrlSerializer, PriceRecommendationsSerializer, VehicleAdSerializer


class RecommendationsByURL(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        url = UrlSerializer.check(request.GET).get('url', None)
        command = Command()
        command.load_defaults()
        command.parse_url(url)
        try:
            ad = VehicleAd.objects.get(url=url)
            similar_ads = VehicleAd.objects.similar_vehicles_for(ad)

            result = {
                'prices': PriceRecommendationsSerializer(similar_ads.define_prices()).data,
                'similar_ads': VehicleAdSerializer(similar_ads, many=True).data
            }
            return Response(result)
        except VehicleAd.DoesNotExist:
            raise Http404()


class VehicleReference(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return Response(
            ReferenceSerializer({
                'brands': Brand.objects.all().prefetch_related('models')
            }).data
        )
