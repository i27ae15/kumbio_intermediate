# Generated by Django 4.1.2 on 2022-11-30 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0028_dayavailableforprofessional'),
        ('authentication_manager', '0002_alter_kumbiotoken_app'),
    ]

    operations = [
        migrations.AddField(
            model_name='kumbiotoken',
            name='organization',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization_info.organization'),
        ),
    ]
