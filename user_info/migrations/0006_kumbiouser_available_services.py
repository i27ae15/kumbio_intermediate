# Generated by Django 4.1.2 on 2022-11-14 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0011_alter_organization_notification_email_and_more'),
        ('user_info', '0005_kumbiouser_available_places'),
    ]

    operations = [
        migrations.AddField(
            model_name='kumbiouser',
            name='available_services',
            field=models.ManyToManyField(blank=True, related_name='available_services', to='organization_info.organizationservice'),
        ),
    ]
