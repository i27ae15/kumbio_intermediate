# Generated by Django 4.1.2 on 2023-01-18 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0044_alter_organizationservice_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationservice',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
