# Generated by Django 4.1.2 on 2022-12-01 05:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization_info', '0030_dayavailableforplace_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organizationclient',
            old_name='created_by',
            new_name='created_by_app',
        ),
        migrations.AddField(
            model_name='organizationclient',
            name='created_by_user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_client_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='organizationclient',
            name='deleted_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_client_deleted_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='organizationclient',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_client_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
