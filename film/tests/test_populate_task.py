from unittest import TestCase
from unittest.mock import patch
import pytest

from codematic.celery import app
from film.contants import SWAPI_FILMS
from film.models import Film
from film.tasks import populate_with_swapi


@pytest.mark.django_db
class TestFilmTasks(TestCase):

    def setUp(self):
        app.conf.update(task_always_eager=True, namespace='CELERY_TEST')

    def test_populate_with_swapi(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {
                "count": 3,
                "results": [
                    {"title": "Film 1", "release_date": "2022-01-01"},
                    {"title": "Film 2", "release_date": "2022-02-02"},
                    {"title": "Film 3", "release_date": "2022-02-03"},
                ],
            }

            # Call the Celery task
            result = populate_with_swapi.apply_async()

            # Check that the task was enqueued successfully
            assert result.successful()
            assert result.result is None

            # Check that the Celery task was called with the correct URL
            mock_get.assert_called_once_with(SWAPI_FILMS)
            # Check that the right amount of data was saved to the db
            assert Film.objects.count() == 3
