# Generated by Django 4.2.2 on 2023-06-24 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport_events', '0002_alter_event_status_alter_payment_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='url',
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]
