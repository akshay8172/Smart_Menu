# Generated by Django 5.1 on 2024-08-30 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Smart_Menu_Application', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restauranttable',
            name='restaurant_address',
        ),
        migrations.RemoveField(
            model_name='restauranttable',
            name='restaurant_name',
        ),
    ]
