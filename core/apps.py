import time
from django.apps import AppConfig
from celery.signals import before_task_publish


def before_task_publish_handler(sender=None, headers=None, body=None, **kwargs):
    headers["__metadata__"] = {"publish_timestamp": time.time()}


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        before_task_publish.connect(before_task_publish_handler)
