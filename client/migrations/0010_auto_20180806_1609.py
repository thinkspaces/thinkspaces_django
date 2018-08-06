# Generated by Django 2.1 on 2018-08-06 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_auto_20180806_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conversants', models.ManyToManyField(related_name='conversations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='conversation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='client.Conversation'),
        ),
    ]
