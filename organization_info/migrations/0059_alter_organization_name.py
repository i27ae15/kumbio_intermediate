# Generated by Django 4.1.2 on 2023-02-01 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0058_alter_organization_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=120, unique=True),
        ),
    ]
