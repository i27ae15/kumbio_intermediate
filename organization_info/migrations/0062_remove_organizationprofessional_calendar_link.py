# Generated by Django 4.1.2 on 2023-02-08 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0061_remove_organizationclient_client_dependent_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organizationprofessional',
            name='calendar_link',
        ),
    ]
