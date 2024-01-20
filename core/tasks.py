import random
import time

from celery import shared_task


@shared_task
def autotune():
    short_duration = random.uniform(0.5, 2)  # Short duration for most tasks
    medium_duration = random.uniform(2, 5)  # Medium duration for 10% of tasks
    long_duration = random.uniform(5, 10)  # Long duration for 1% of tasks (P99)

    probability = random.random()

    if probability < 0.90:
        time_to_sleep = short_duration
    elif probability < 0.99:
        time_to_sleep = medium_duration
    else:
        time_to_sleep = long_duration

    time.sleep(time_to_sleep)
