from django.db import models

from shared.choices import KEYBOARD_TYPE_CHOICES, LANGUAGE_CHOICES
from shared.db import nb
from shared.enums import LanguageCode
from tgbot.shared.enums import KeyboardType


# Create your models here.

class TelegramUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=32)
    full_name = models.CharField(max_length=255, **nb)
    phone = models.CharField(max_length=16, **nb)
    email = models.EmailField()
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default=LanguageCode.RU.value)


class Keyboard(models.Model):
    key = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=10, choices=KEYBOARD_TYPE_CHOICES, default=KeyboardType.REPLY)

    def __str__(self):
        return self.key


class ButtonBase(models.Model):
    text_ru = models.CharField(max_length=255)
    text_kz = models.CharField(max_length=255, default='', **nb)
    key = models.CharField(max_length=255, default='', **nb)
    order = models.PositiveBigIntegerField(default=0)
    hidden = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ReplyButton(ButtonBase):
    keyboard = models.ForeignKey(Keyboard, on_delete=models.CASCADE, related_name='reply_buttons')
    request_contact = models.BooleanField(default=False)
    request_location = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.keyboard.key} -> {self.text_ru}"


class InlineButton(ButtonBase):
    keyboard = models.ForeignKey(Keyboard, on_delete=models.CASCADE, related_name='inline_buttons')
    url_ru = models.URLField(max_length=1000, default='', **nb)
    url_kz = models.URLField(max_length=1000, default='', **nb)
    callback_data = models.CharField(max_length=255, default='', **nb)

    def __str__(self):
        return f"{self.keyboard.key} -> {self.text_ru}"


class MessageText(models.Model):
    key = models.CharField(max_length=255, unique=True)
    text_ru = models.TextField()
    text_kz = models.TextField(**nb)
