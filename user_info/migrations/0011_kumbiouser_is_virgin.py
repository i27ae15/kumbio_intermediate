# Generated by Django 4.1.2 on 2023-03-27 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0010_todolist_todolisttask'),
    ]

    operations = [
        migrations.AddField(
            model_name='kumbiouser',
            name='is_virgin',
            field=models.BooleanField(default=True),
        ),
    ]