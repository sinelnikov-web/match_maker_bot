import uuid

from django.db import models

from shared.choices import PAYMENT_STATUS_CHOICE, EVENT_STATUS_CHOICE
from shared.db import nb
from shared.enums import EventStatus, PaymentStatus
from telegram.models import TelegramUser


# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(**nb)
    image = models.ImageField(**nb)
    host = models.ForeignKey(TelegramUser, on_delete=models.PROTECT, related_name='events_as_host')
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    max_participants = models.IntegerField()
    status = models.CharField(max_length=40, choices=EVENT_STATUS_CHOICE, default=EventStatus.PARTICIPANTS_WAIT.value)


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='teams')
    participants = models.ManyToManyField(TelegramUser, related_name='teams')


class Payment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='payments')
    user = models.ForeignKey(TelegramUser, on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    url = models.URLField(**nb, default=None)
    status = models.CharField(max_length=40, choices=PAYMENT_STATUS_CHOICE, default=PaymentStatus.PENDING.value)
