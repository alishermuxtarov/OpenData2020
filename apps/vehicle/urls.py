from django.urls import path

from vehicle.views import RecommendationsByURL

urlpatterns = [
    path('buyer/recommendations_by_url/', RecommendationsByURL.as_view(), name='buyer-recommendations-by-url'),
]
