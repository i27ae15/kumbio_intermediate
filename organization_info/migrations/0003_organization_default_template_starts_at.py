# Generated by Django 4.1.2 on 2022-11-01 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='default_template_starts_at',
            field=models.IntegerField(default=0),
        ),
    ]
