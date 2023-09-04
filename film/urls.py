from django.urls import path, include
from rest_framework.routers import DefaultRouter

from film.views import FilmsViewSet

router = DefaultRouter()
router.register(r'', FilmsViewSet, basename='films')

urlpatterns = [
    path('', include(router.urls)),
]