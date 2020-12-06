from django.db.models import QuerySet
from django.db.models.aggregates import Count, Max, Min, Avg


class VehicleAdQueryset(QuerySet):
    def similar_vehicles(self, model, manufactured_year, transmission_type, condition, driven_km):
        qs = self.filter(model=model)

        if manufactured_year:
            qs = qs.filter(manufactured_year=manufactured_year)

        if transmission_type:
            qs = qs.filter(transmission_type=transmission_type)

        if condition:
            qs = qs.filter(condition=condition)

        if driven_km:
            qs = qs.filter(driven_km__range=[driven_km - 10000, driven_km + 10000])

        return qs

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

    def stats_by_model_and_manufactured_year(self, model_id):
        return self.raw(
            """
            select a.*, a.model_id as id from (
                select a.model_id, a.manufactured_year,
                       round(avg(price_usd)) avg_price_usd,
                       round(avg(price_uzs)) avg_price_uzs
                from vehicle_ads a
                where model_id = {model_id} and transmission_type = 'automatic'
                group by a.model_id, a.manufactured_year
                order by a.model_id, a.manufactured_year
            ) a order by a.model_id, a.manufactured_year, a.avg_price_usd;
            """.format(model_id=model_id)
        )

    def stats_by_model_and_driven_km(self, model_id):
        return self.raw(
            """
            select a.model_id as id, a.driven_km * 5000 as driven_km, a.avg_price_usd, avg_price_uzs from (
                select
                   a.model_id,
                   a.driven_km,
                   round(avg(price_usd)) avg_price_usd,
                   round(avg(price_uzs)) avg_price_uzs
               from (
                    select model_id, round(driven_km/1000/5) as driven_km, price_uzs, price_usd
                    from vehicle_ads
                    where model_id = {model_id} and transmission_type = 'automatic'
                ) a
                group by a.model_id, a.driven_km
                order by a.model_id, a.driven_km
            ) a
            """.format(model_id=model_id)
        )

    def recommendations(self, model_id, manufactured_year, transmission_type, condition, driven_km):
        similar_ads = self.similar_vehicles(
            model_id,
            manufactured_year,
            transmission_type,
            condition,
            driven_km
        )
        stats_by_manufactured_year = self.stats_by_model_and_manufactured_year(model_id)
        stats_by_driven_km = self.stats_by_model_and_driven_km(model_id)

        return {
            'prices': similar_ads.define_prices(),
            'similar_ads': similar_ads[:20],
            'similar_ads_total': similar_ads.count(),
            'stats_by_manufactured_year': stats_by_manufactured_year,
            'stats_by_driven_km': stats_by_driven_km
        }
