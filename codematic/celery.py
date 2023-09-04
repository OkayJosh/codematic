import os
from datetime import timedelta

from celery import Celery
import logging

from decouple import config

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codematic.settings')


app = Celery('codematicapi', broker=config('REDIS_URL'))


# Load the celery settings from the Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

LOG = logging.getLogger(__name__)

app.conf.beat_schedule = {
    'social-task': {
        'task': 'film.tasks.populate_with_swapi',
        'schedule': timedelta(seconds=5550),  # Run every 5550 seconds
    },
}
