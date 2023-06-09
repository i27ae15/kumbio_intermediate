# Generated by Django 4.1.2 on 2022-12-15 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0038_rename_day_dayavailableforprofessional_professional_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationprofessional',
            name='place',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization_info.organizationplace'),
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
