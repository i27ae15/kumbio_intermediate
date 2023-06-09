# Generated by Django 4.1.2 on 2022-11-27 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0018_kumbiotoken_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayavailableforplace',
            name='exclude',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='organizationclient',
            name='birth_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='organizationclient',
            name='comments',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='organizationclient',
            name='emergency_contact',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='organizationclient',
            name='identification',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='organizationclient',
            name='rating',
            field=models.IntegerField(blank=True, default=None, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='organizationclientdependent',
            name='phone_2',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]
