import redis

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import autotune


@csrf_exempt
def enqueue_autotune_task(request):
    if request.method == "POST":
        result = autotune.delay()
        return JsonResponse(
            {"task_id": result.task_id, "status": "Task submitted successfully!"},
            status=200,
        )
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)


def max_queue_wait_time(request):
    redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

    max_time_data = redis_client.zrevrange("task_elapsed_times", 0, 0, withscores=True)
    max_elapsed_time = max_time_data[0][1] if max_time_data else 0

    return JsonResponse({"max_elapsed_time": max_elapsed_time})
