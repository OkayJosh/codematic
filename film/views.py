from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from film.models import Film, Comment
from film.serializers import FilmsSerializer, CommentsSerializer
from film.tasks import populate_with_swapi


# class AccountViewsSet(ViewSet):
#     login_serializer_class = AuthTokenSerializer
#     signup_serializer_class = SignupSerializer
#

class FilmsViewSet(ViewSet):
    film_serializer_class = FilmsSerializer
    comment_serializer_class = CommentsSerializer
    pagination_class = PageNumberPagination

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    @action(methods=['GET'], detail=False, )
    def films(self, request):
        """get list of films"""
        data = Film.objects.all().order_by('-release_date').values()
        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.film_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.film_serializer_class(data, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, )
    def comments(self, request):
        """get list of comments"""
        self.name = "Comment"
        self.description = "List of comments"
        """get list comments for a film"""
        data = Comment.objects.all().order_by('-created')
        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.comment_serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.comment_serializer_class(data, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False, )
    def comment_add(self, request):
        """add a comment to a film"""
        self.name = "Add Comment"
        self.description = "Post comments"
        data = request.data
        serializer = self.comment_serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'message', 'comment not created'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message', 'comment created'}, status=status.HTTP_201_CREATED)

    @action(methods=['PUT'], detail=True)  # PUT for updating a film
    def film_update(self, request, pk):
        try:
            film = Film.objects.get(pk=pk)
        except Film.DoesNotExist:
            return Response({'message': 'Film not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.film_serializer_class(film, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Film updated'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid data for updating film'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=True)  # DELETE for deleting a film
    def film_delete(self, request, pk):
        try:
            film = Film.objects.get(pk=pk)
        except Film.DoesNotExist:
            return Response({'message': 'Film not found'}, status=status.HTTP_404_NOT_FOUND)

        film.delete()
        return Response({'message': 'Film deleted'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['PUT'], detail=True)  # PUT for updating a comment
    def comment_update(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({'message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.comment_serializer_class(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Comment updated'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid data for updating comment'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=True)  # DELETE for deleting a comment
    def comment_delete(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({'message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response({'message': 'Comment deleted'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['GET'])
    def comments_for_film(self, request, pk=None):
        try:
            film = Film.objects.get(pk=pk)
        except Film.DoesNotExist:
            return Response({'message': 'Film not found'}, status=status.HTTP_404_NOT_FOUND)

        data = Comment.objects.filter(film=film).order_by('created')
        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.comment_serializer_class(data, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.comment_serializer_class(data, many=True)

        return Response(serializer.data)

    @action(methods=['POST'], detail=False, )
    def swapi_callback(self, request):
        """webhook to get updates"""
        data = request.data

        if data.get("event", None) == "update":
            # run update on the database
            populate_with_swapi.delay()
            return Response({'message', 'update received'}, status=status.HTTP_200_OK)
        else:
            # ignore
            return Response({'message', 'event received'}, status=status.HTTP_200_OK)