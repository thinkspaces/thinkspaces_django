# Generated by Django 2.1 on 2018-08-19 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0024_auto_20180818_0209'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cover_image',
            field=models.URLField(blank=True),
        ),
    ]
