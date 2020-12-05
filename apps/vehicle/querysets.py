from django.db.models import QuerySet
from django.db.models.aggregates import Count, Max, Min, Avg


class VehicleAdQueryset(QuerySet):
    def similar_vehicles_for(self, ad):
        return self.similar_vehicles(
            brand=ad.brand,
            model=ad.model,
            manufactured_year=ad.manufactured_year,
            transmission_type=ad.transmission_type,
            condition=ad.condition,
            driven_km=ad.driven_km
        )

    def similar_vehicles(self, brand, model, manufactured_year, transmission_type, condition, driven_km):
        return self.filter(
            brand=brand,
            model=model,
            # manufactured_year__in=[ad.manufactured_year - 1, ad.manufactured_year, ad.manufactured_year + 1],
            manufactured_year=manufactured_year,
            transmission_type=transmission_type,
            condition=condition,
            driven_km__range=[driven_km - 10000, driven_km + 10000]
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
