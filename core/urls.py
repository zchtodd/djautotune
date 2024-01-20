from django.urls import path
from . import views

urlpatterns = [
    path("autotune/", views.enqueue_autotune_task, name="enqueue_autotune_task"),
    path("queue/wait/", views.max_queue_wait_time, name="max_queue_wait_time"),
]
