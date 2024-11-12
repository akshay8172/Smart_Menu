# Generated by Django 5.0.7 on 2024-08-27 14:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LoginTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='Pending', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField(unique=True)),
                ('qr_code_url', models.URLField(blank=True, null=True)),
                ('restaurant_name', models.CharField(max_length=100)),
                ('restaurant_address', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('phone', models.BigIntegerField()),
                ('email', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=10)),
                ('date_of_birth', models.DateField()),
                ('photo', models.ImageField(upload_to='delivery_staff_images/')),
                ('LOGIN_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Smart_Menu_Application.logintable')),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('image', models.ImageField(upload_to='menu_images/')),
                ('is_available', models.BooleanField(default=True)),
                ('CATEGORY_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Smart_Menu_Application.category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('MENU_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Smart_Menu_Application.menuitem')),
                ('ORDER_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Smart_Menu_Application.order')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(max_length=50)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('paid_at', models.DateTimeField(blank=True, null=True)),
                ('ORDER_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Smart_Menu_Application.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='TABLE',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Smart_Menu_Application.restauranttable'),
        ),
    ]
