# Generated by Django 5.1 on 2024-08-30 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Smart_Menu_Application', '0002_remove_restauranttable_restaurant_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restauranttable',
            name='qr_code_url',
        ),
        migrations.AddField(
            model_name='restauranttable',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='qr_codes/'),
        ),
    ]
