from django.db.models import QuerySet
from django.db.models.aggregates import Count, Max, Min, Avg


class VehicleAdQueryset(QuerySet):
    def similar_vehicles(self, ad):
        return self.filter(
            region=ad.region,
            area=ad.area,
            brand=ad.brand,
            model=ad.model,
            # manufactured_year__in=[ad.manufactured_year - 1, ad.manufactured_year, ad.manufactured_year + 1],
            manufactured_year=ad.manufactured_year,
            transmission_type=ad.transmission_type,
            condition=ad.condition,
            driven_km__range=[ad.driven_km - 10000, ad.driven_km + 10000]
        )

    def define_prices(self):
        return self.aggregate(
            ads_count=Count('id'),
            max_price_uzs=Max('price_uzs'),
            min_price_uzs=Min('price_uzs'),
            avg_price_uzs=Avg('price_uzs'),
            max_price_usd=Max('price_usd'),
            min_price_usd=Min('price_usd'),
            avg_price_usd=Avg('price_usd'),
        )
