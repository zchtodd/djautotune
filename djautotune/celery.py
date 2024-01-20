import time
import os
import redis

from celery import Celery
from celery.signals import task_prerun
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djautotune.settings")

app = Celery("djautotune")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


@task_prerun.connect
def task_prerun_handler(task_id, task, *args, **kwargs):
    metadata = getattr(task.request, "__metadata__", {})
    publish_timestamp = metadata.get("publish_timestamp")

    if publish_timestamp:
        elapsed_time = time.time() - publish_timestamp

        redis_client.zadd("task_elapsed_times", {task_id: elapsed_time})
        redis_client.expire("task_elapsed_times", settings.CELERY_METRICS_TTL, nx=True)
