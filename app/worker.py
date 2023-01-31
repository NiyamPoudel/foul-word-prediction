import os
import sys
from celery import Celery
# import app.settings as env

CELERY_BROKER_URL ='redis://127.0.0.1:6379/0'
# 'redis://127.0.0.1:6379'

celery = Celery(
    "processor",
    broker=CELERY_BROKER_URL
)

celery.conf.update(
    #CELERY_ACKS_LATE=True,
    CELERYD_PREFETCH_MULTIPLIER=16,
    BROKER_POOL_LIMIT=None,
    BROKER_CONNECTION_MAX_RETRIES=None
)
