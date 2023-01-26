# Generated by Django 4.1.2 on 2023-01-26 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0007_notificationssettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='kumbiouser',
            name='code_to_recover_password',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='kumbiouser',
            name='code_to_recover_password_date_expiration',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
