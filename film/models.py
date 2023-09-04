import uuid
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Film(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=200, blank=True, null=True)
    release_date = models.DateTimeField(blank=True, null=True)


class Comment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # text length limited to 500 characters
    text = models.CharField(max_length=500, blank=True, null=True)
    film = models.ForeignKey(
        'Film', on_delete=models.SET_NULL, related_name="film_comments", null=True, blank=True
    )
