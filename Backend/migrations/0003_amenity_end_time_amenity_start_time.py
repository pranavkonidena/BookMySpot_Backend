# Generated by Django 4.2.4 on 2023-09-28 16:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0002_remove_team_admin_id_team_admin_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='amenity',
            name='end_time',
            field=models.TimeField(default=datetime.time(22, 0)),
        ),
        migrations.AddField(
            model_name='amenity',
            name='start_time',
            field=models.TimeField(default=datetime.time(8, 0)),
        ),
    ]
