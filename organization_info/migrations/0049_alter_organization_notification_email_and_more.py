# Generated by Django 4.1.2 on 2023-01-26 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0048_dayavailableforprofessional_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='notification_email',
            field=models.EmailField(default='default@email.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='organization',
            name='notification_email_password',
            field=models.BinaryField(default=b'defaultemailpassword'),
        ),
    ]