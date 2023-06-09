# Generated by Django 4.1.2 on 2022-12-18 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0039_organizationprofessional_place_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationclient',
            name='send_marketing_by_email',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='organizationclient',
            name='send_marketing_by_sms',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='organizationclient',
            name='send_marketing_by_whatsapp',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='organizationclient',
            name='send_notifications_by_email',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='organizationclient',
            name='send_notifications_by_sms',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='organizationclient',
            name='send_notifications_by_whatsapp',
            field=models.BooleanField(default=True),
        ),
    ]
