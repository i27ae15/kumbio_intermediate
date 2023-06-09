# Generated by Django 4.1.2 on 2022-11-09 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization_info', '0008_rename_payment_methods_organizationplace_payment_methods_accepted_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailtemplate',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='mailtemplate',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='mailtemplate',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='MailTemplatesManager',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='default_template_starts_at',
        ),
        migrations.AddField(
            model_name='organization',
            name='email_templates',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='calendarsettings',
            name='template_to_send_as_canceled',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='calendarsettings',
            name='template_to_send_as_canceled_to_calendar_user',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='calendarsettings',
            name='template_to_send_as_confirmation',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='calendarsettings',
            name='template_to_send_as_new_client_to_calendar_user',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='calendarsettings',
            name='template_to_send_as_reminder_1',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='calendarsettings',
            name='template_to_send_as_reminder_2',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='calendarsettings',
            name='template_to_send_as_reminder_3',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='calendarsettings',
            name='template_to_send_as_rescheduled',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='calendarsettings',
            name='template_to_send_as_rescheduled_to_calendar_user',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.DeleteModel(
            name='MailTemplate',
        ),
    ]
