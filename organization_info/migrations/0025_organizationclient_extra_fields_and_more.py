# Generated by Django 4.1.2 on 2022-11-28 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0024_alter_organizationclient_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationclient',
            name='extra_fields',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='organizationclienttype',
            name='fields',
            field=models.JSONField(default=list),
        ),
    ]
