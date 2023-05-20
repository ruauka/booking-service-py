from celery import Celery

from config import cfg

# движок celery
celery = Celery(
    "tasks",
    broker=f"redis://{cfg.REDIS_HOST}:{cfg.REDIS_PORT}",
    include=["app.tasks.tasks"]
)
