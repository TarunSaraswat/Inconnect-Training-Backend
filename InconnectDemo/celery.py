from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'InconnectDemo.settings')
app = Celery('InconnectDemo')

app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')
# Celery Beat Settings
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'User.tasks.report_generator',
        'schedule': 30.0,
        'args': ()
    },
}

app.autodiscover_tasks()
