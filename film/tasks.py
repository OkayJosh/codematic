import logging

import requests
from celery import shared_task

from film.contants import SWAPI_FILMS, MAX_RETRY_ATTEMPTS, RETRY_DELAY
from film.models import Film

LOG = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=MAX_RETRY_ATTEMPTS, retry_backoff=RETRY_DELAY)
def populate_with_swapi(*args, **kwargs):
    try:
        response = requests.get(SWAPI_FILMS)
        LOG.info(f'{SWAPI_FILMS} called with response {response.status_code}')
        response.raise_for_status()
        if response.json()['count'] >= Film.objects.count():
            return
        else:
            data = response.json()['results']
            for value in data:
                films = Film.objects.filter(title=value['title'])
                if not films.exists():
                    Film.objects.create(title=value['title'], release_date=value['release_date'])

            return
    except requests.exceptions.Timeout as e:
        LOG.exception(e)
        raise self.retry()
