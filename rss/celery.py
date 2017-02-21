import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_django_rss.settings')
app = Celery(broker='redis://localhost')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


if __name__ == '__main__':
    app.start()
