# Generated by Django 2.1 on 2018-08-06 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_unread',
            field=models.BooleanField(default=True),
        ),
    ]
