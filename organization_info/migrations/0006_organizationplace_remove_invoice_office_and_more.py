# Generated by Django 4.1.2 on 2022-11-02 17:24

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization_info', '0005_remove_organizationprofessional_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('accepts_children', models.BooleanField(default=True)),
                ('accepts_pets', models.BooleanField(default=True)),
                ('additional_info', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('opens_at', models.TimeField(default=datetime.time(8, 0))),
                ('closes_at', models.TimeField(default=datetime.time(18, 0))),
                ('photo', models.CharField(blank=True, max_length=255, null=True)),
                ('local_timezone', models.CharField(default='America/Bogota', max_length=120)),
                ('datetime_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('datetimne_updated', models.DateTimeField(blank=True, default=None, null=True)),
                ('datetime_deleted', models.DateTimeField(blank=True, default=None, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='office_created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='office_deleted_by', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization_info.organization')),
                ('payment_methods', models.ManyToManyField(blank=True, to='organization_info.paymentmethodacceptedbyorg')),
                ('services', models.ManyToManyField(to='organization_info.organizationservice')),
                ('updated_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='office_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='office',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='deleted_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice_deleted_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='updated_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoice_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='OrganizationOffice',
        ),
        migrations.AddField(
            model_name='invoice',
            name='place',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization_info.organizationplace'),
        ),
    ]
