# Generated by Django 2.2.5 on 2019-10-29 19:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0003_room_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_reservation', models.DateField()),
                ('end_reservation', models.DateField()),
                ('price_reservation', models.IntegerField()),
                ('id_customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_customer', to=settings.AUTH_USER_MODEL)),
                ('id_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.Room')),
                ('id_staff', models.ForeignKey(blank=True, null=True, on_delete=models.SET('<django.db.models.query_utils.DeferredAttribute object at 0x0421F8B0> <django.db.models.query_utils.DeferredAttribute object at 0x0421F8D0>'), related_name='id_staff', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
