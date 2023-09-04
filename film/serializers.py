from rest_framework import serializers

from film.models import Film, Comment


class FilmsSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Film
        fields = [
            'id', 'title', 'release_date',
            'comment_count',
        ]

    def get_comment_count(self, obj):
        return Comment.objects.filter(film__id=obj['id']).count()


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id', 'text', 'film'
        ]
