# Generated by Django 4.1.2 on 2023-01-26 13:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_manager', '0004_clientdashboardtoken_alter_kumbiotoken_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientdashboardtoken',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
