# Generated by Django 4.1.2 on 2023-02-09 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0062_remove_organizationprofessional_calendar_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='default_timezone',
            field=models.CharField(blank=True, default=None, max_length=120, null=True),
        ),
    ]
