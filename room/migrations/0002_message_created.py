# Generated by Django 4.0.2 on 2022-02-16 22:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 2, 16, 22, 22, 37, 216719)),
            preserve_default=False,
        ),
    ]
