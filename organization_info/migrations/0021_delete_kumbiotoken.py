# Generated by Django 4.1.2 on 2022-11-27 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0020_alter_organizationclient_rating'),
    ]

    operations = [
        migrations.DeleteModel(
            name='KumbioToken',
        ),
    ]
