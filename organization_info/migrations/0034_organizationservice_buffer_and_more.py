# Generated by Django 4.1.2 on 2022-12-02 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0033_remove_organizationclient_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationservice',
            name='buffer',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='organizationservice',
            name='conditions_and_discounts',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='organizationservice',
            name='only_booking',
            field=models.BooleanField(default=True),
        ),
    ]
