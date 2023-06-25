# Generated by Django 4.2.2 on 2023-06-24 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('telegram', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('date', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('max_participants', models.IntegerField()),
                ('status', models.CharField(choices=[('participants_wait', 'Ожидание участников'), ('payment_wait', 'Ожидание оплаты'), ('paid', 'Оплачен'), ('caneled', 'Отменён')], max_length=40)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='events_as_host', to='telegram.telegramuser')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teams', to='sport_events.event')),
                ('participants', models.ManyToManyField(related_name='teams', to='telegram.telegramuser')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('status', models.CharField(choices=[('payment_wait', 'Ожидание оплаты'), ('paid', 'Оплачено'), ('caneled', 'Отменено')], max_length=40)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='sport_events.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='telegram.telegramuser')),
            ],
        ),
    ]
