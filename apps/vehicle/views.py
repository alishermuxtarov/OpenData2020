from django.http import Http404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from vehicle.management.commands.aggregate import Command
from vehicle.models import VehicleAd, Brand, Model
from vehicle.serlializers.reference import ReferenceSerializer
from vehicle.serlializers.vehicle import UrlSerializer, PriceRecommendationsSerializer, VehicleAdSerializer, \
    AvgPriceByManufacturedYearSerializer, AvgPriceByDrivenKmSerializer, VehicleParametersValidator


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
                'current_ad': VehicleAdSerializer(ad).data,
                'prices': PriceRecommendationsSerializer(recommendations.get('prices')).data,
                'similar_ads': VehicleAdSerializer(recommendations.get('similar_ads'), many=True).data,
                'similar_ads_total': recommendations.get('similar_ads_total'),
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


class RecommendationsByParameters(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        parameters = VehicleParametersValidator.check(request.GET)
        model = None
        model_name = parameters.get('model_name', None)
        model_id = parameters.get('model_id', None)
        manufactured_year = parameters.get('manufactured_year', None)
        transmission_type = parameters.get('transmission_type', None)
        condition = parameters.get('condition', None)
        driven_km = parameters.get('driven_km', None)

        if model_name:
            model = Model.objects.filter(name__iexact=model_name).first()

        if not model and model_id:
            model = Model.objects.filter(pk=model_id).first()

        if not model:
            raise Http404()
        else:
            model_id = model.pk

        try:
            parameters.pop('model_id')
            parameters.pop('model_name')
        except KeyError:
            pass

        recommendations = VehicleAd.objects.recommendations(
            model_id,
            manufactured_year,
            transmission_type,
            condition,
            driven_km
        )

        result = {
            'prices': PriceRecommendationsSerializer(recommendations.get('prices')).data,
            'similar_ads': VehicleAdSerializer(recommendations.get('similar_ads'), many=True).data,
            'similar_ads_total': recommendations.get('similar_ads_total'),
            'stats_by_manufactured_year': AvgPriceByManufacturedYearSerializer(
                recommendations.get('stats_by_manufactured_year'), many=True
            ).data,
            'stats_by_driven_km': AvgPriceByDrivenKmSerializer(
                recommendations.get('stats_by_driven_km'), many=True
            ).data
        }
        return Response(result)


class VehicleReference(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return Response(
            ReferenceSerializer({
                'brands': Brand.objects.all().prefetch_related('models')
            }).data
        )
