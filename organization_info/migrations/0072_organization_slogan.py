# Generated by Django 4.1.2 on 2023-03-23 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0071_organizationclienttype_spanish_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='slogan',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True),
        ),
    ]
