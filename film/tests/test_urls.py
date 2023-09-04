from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from film.models import Film


class FilmsViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.film1 = Film.objects.create(title="Film 1", release_date="2022-01-01")
        self.film2 = Film.objects.create(title="Film 2", release_date="2021-01-01")

    def test_get_films(self):
        response = self.client.get('/films/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_comments_for_film(self):
        response = self.client.get(f'/{self.film1.id}/comments_for_film/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_comment_to_film(self):
        data = {"text": "This is a comment."}
        response = self.client.post(f'/comment_add/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_comments_for_nonexistent_film(self):
        response = self.client.get('/aca1fc94-156e-4500-be4c-418be419cdc4/comments_for_film/')  # Assuming film with ID 999 doesn't exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
