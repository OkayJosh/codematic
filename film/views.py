from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from film.models import Film, Comment
from film.serializers import FilmsSerializer, CommentsSerializer


# class AccountViewsSet(ViewSet):
#     login_serializer_class = AuthTokenSerializer
#     signup_serializer_class = SignupSerializer
#

class FilmsViewSet(ViewSet):
    film_serializer_class = FilmsSerializer
    comment_serializer_class = CommentsSerializer

    @action(methods=['GET'], detail=False, )
    def films(self):
        """get list of films"""
        data = Film.objects.all().order_by('-release_date')
        serializer = self.film_serializer_class(data=data)
        return Response(data=serializer.data)

    @action(methods=['GET'], detail=False, )
    def comments(self):
        """get list comments for a film"""
        data = Comment.objects.all().order_by('-created')
        serializer = self.comment_serializer_class(data=data)
        return Response(data=serializer.data)

    @action(methods=['POST'], detail=False, )
    def comment_add(self, request):
        """add a comment to a film"""
        data = request.data
        serializer = self.comment_serializer_class(data=data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
        else:
            return Response({'message', 'comment not created'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message', 'comment created'}, status=status.HTTP_201_CREATED)

    # PUT comment
    # Delete comment
    # PUT film
    # Delete Film
