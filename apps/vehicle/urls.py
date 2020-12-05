from django.urls import path

from vehicle.views import RecommendationsByURL, VehicleReference

urlpatterns = [
    path('reference/', VehicleReference.as_view(), name='reference'),
    path('buyer/recommendations_by_url/', RecommendationsByURL.as_view(), name='buyer-recommendations-by-url'),
]
