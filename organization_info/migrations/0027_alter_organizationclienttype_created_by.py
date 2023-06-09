# Generated by Django 4.1.2 on 2022-11-28 02:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization_info', '0026_alter_organizationclienttype_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationclienttype',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_type_created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
