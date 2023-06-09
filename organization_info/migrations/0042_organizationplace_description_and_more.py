# Generated by Django 4.1.2 on 2023-01-18 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0041_alter_organization_notification_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationplace',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='notification_email',
            field=models.EmailField(default='Email', max_length=254),
        ),
        migrations.AlterField(
            model_name='organization',
            name='notification_email_password',
            field=models.BinaryField(default=b'password'),
        ),
    ]
