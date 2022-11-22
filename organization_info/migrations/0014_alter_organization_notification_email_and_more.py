# Generated by Django 4.1.2 on 2022-11-18 17:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0013_organization_template_to_send_as_canceled_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='notification_email',
            field=models.EmailField(default='Email', max_length=254),
        ),
        migrations.AlterField(
            model_name='organization',
            name='notification_email_password',
            field=models.BinaryField(default=b'password'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='sector',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization_info.sector'),
        ),
        migrations.AlterField(
            model_name='organizationplace',
            name='additional_info',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='organizationplace',
            name='address',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='organizationplace',
            name='closes_at',
            field=models.TimeField(blank=True, default=datetime.time(18, 0), null=True),
        ),
        migrations.AlterField(
            model_name='organizationplace',
            name='custom_price',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='organizationplace',
            name='email',
            field=models.EmailField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='organizationplace',
            name='local_timezone',
            field=models.CharField(blank=True, default='', max_length=120),
        ),
        migrations.AlterField(
            model_name='organizationplace',
            name='opens_at',
            field=models.TimeField(blank=True, default=datetime.time(8, 0), null=True),
        ),
        migrations.AlterField(
            model_name='organizationplace',
            name='phone',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='organizationplace',
            name='photo',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]