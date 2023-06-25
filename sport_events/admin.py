from django.contrib import admin

from sport_events.models import Event, Team, Payment


# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'status', 'host', 'amount']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'event']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'status']