# Generated by Django 4.2.4 on 2023-10-02 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0021_remove_groupbooking_name_of_slot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='individualbooking',
            name='name_of_slot',
        ),
    ]
