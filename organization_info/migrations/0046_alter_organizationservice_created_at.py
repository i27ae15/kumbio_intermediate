# Generated by Django 4.1.2 on 2023-01-18 18:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0045_alter_organizationservice_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationservice',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
