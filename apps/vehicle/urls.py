from django.urls import path

from vehicle.views import RecommendationsByURL, VehicleReference, RecommendationsByParameters

urlpatterns = [
    path('reference/', VehicleReference.as_view(), name='reference'),
    path('buyer/recommendations_by_url/', RecommendationsByURL.as_view(), name='buyer-recommendations-by-url'),
    path('buyer/recommendations_by_parameters/', RecommendationsByParameters.as_view(), name='buyer-recommendations-by-parameters'),
]
