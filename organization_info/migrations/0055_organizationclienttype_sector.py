# Generated by Django 4.1.2 on 2023-02-01 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0054_remove_organizationclienttype_sector'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationclienttype',
            name='sector',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sector', to='organization_info.sector'),
        ),
    ]