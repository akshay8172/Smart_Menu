# Generated by Django 5.1 on 2024-10-03 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Smart_Menu_Application', '0008_delete_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
