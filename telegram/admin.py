from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from telegram.models import TelegramUser, MessageText, ReplyButton, InlineButton, Keyboard


# Register your models here.

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']


class InlineButtonStackedInline(admin.StackedInline):
    extra = 2
    model = InlineButton


class ReplyButtonStackedInline(admin.StackedInline):
    extra = 2
    model = ReplyButton


@admin.register(Keyboard)
class KeyboardAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['key', 'type']
    inlines = [ReplyButtonStackedInline, InlineButtonStackedInline]


@admin.register(InlineButton)
class InlineButtonAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['text_ru', 'callback_data', 'url_ru']


@admin.register(ReplyButton)
class ReplyButtonAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['text_ru', 'request_contact', 'request_location']


@admin.register(MessageText)
class MessageTextAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['key', 'text_ru']
