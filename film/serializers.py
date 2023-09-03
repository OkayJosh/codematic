from rest_framework import serializers

from film.models import Film, Comment


class FilmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = [
            'id', 'title', 'release_date',
            'comment_count',
        ]


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id', 'text', 'film__id'
        ]
