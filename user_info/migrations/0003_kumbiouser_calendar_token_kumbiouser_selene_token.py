# Generated by Django 4.1.2 on 2022-11-01 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0002_remove_kumbiouser_default_template_starts_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='kumbiouser',
            name='calendar_token',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='kumbiouser',
            name='selene_token',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]