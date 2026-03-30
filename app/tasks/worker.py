from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "disney_bot",
    broker=settings.broker_url,
    backend=settings.result_backend,
)

celery_app.conf.task_routes = {"app.tasks.jobs.*": {"queue": "disney_bot"}}
celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"
celery_app.conf.accept_content = ["json"]
celery_app.conf.worker_send_task_events = True
