# Generated by Django 5.1 on 2024-10-03 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Smart_Menu_Application', '0014_alter_order_order_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateField(auto_now_add=True),
        ),
    ]
