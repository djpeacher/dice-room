# Generated by Django 4.0.2 on 2022-02-11 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.CharField(max_length=128)),
                ('user', models.CharField(max_length=128)),
                ('message', models.TextField()),
            ],
        ),
    ]
