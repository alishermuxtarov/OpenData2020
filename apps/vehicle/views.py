from django.http import Http404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from vehicle.management.commands.aggregate import Command
from vehicle.models import VehicleAd, Brand
from vehicle.serlializers.reference import ReferenceSerializer
from vehicle.serlializers.vehicle import UrlSerializer, PriceRecommendationsSerializer, VehicleAdSerializer, \
    AvgPriceByManufacturedYearSerializer, AvgPriceByDrivenKmSerializer, RecommendationSerializer


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

            recommendations = VehicleAd.objects.recommendations(
                ad.model_id, ad.manufactured_year, ad.transmission_type, ad.condition, ad.driven_km
            )

            result = {
                'prices': PriceRecommendationsSerializer(recommendations.get('prices')).data,
                'similar_ads': VehicleAdSerializer(recommendations.get('similar_ads'), many=True).data,
                'stats_by_manufactured_year': AvgPriceByManufacturedYearSerializer(
                    recommendations.get('stats_by_manufactured_year'), many=True
                ).data,
                'stats_by_driven_km': AvgPriceByDrivenKmSerializer(
                    recommendations.get('stats_by_driven_km'), many=True
                ).data
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
