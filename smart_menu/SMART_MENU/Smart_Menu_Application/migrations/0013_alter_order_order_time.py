# Generated by Django 5.1 on 2024-10-03 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Smart_Menu_Application', '0012_order_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(),
        ),
    ]