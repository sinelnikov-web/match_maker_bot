import asyncio
import os

import django
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'match_maker_bot.settings')
django.setup()

from tgbot.settings.env import REDIS_IP

celery_event_loop = asyncio.new_event_loop()

celery_app = Celery("match_maker_bot", broker=f"redis://{REDIS_IP}:6379", include=['sport_events.tasks'])
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
