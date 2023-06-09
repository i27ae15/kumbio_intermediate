# Generated by Django 4.1.2 on 2022-11-14 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0010_organizationplace_custom_price_and_more'),
        ('user_info', '0004_kumbiouser_extra_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='kumbiouser',
            name='available_places',
            field=models.ManyToManyField(blank=True, related_name='available_places', to='organization_info.organizationplace'),
        ),
    ]
