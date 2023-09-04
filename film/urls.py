from django.urls import path

from film.views import FilmsViewSet

urlpatterns = [
    path("films/", FilmsViewSet.as_view({'get': 'films'}), name="films"),
    path("comments/", FilmsViewSet.as_view({'get': 'comments', 'post': 'comment_add'}), name="comments"),
]