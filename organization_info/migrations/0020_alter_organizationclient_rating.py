# Generated by Django 4.1.2 on 2022-11-27 18:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0019_alter_dayavailableforplace_exclude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationclient',
            name='rating',
            field=models.IntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(100)]),
        ),
    ]