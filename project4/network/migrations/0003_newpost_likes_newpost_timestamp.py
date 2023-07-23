# Generated by Django 4.0.2 on 2022-04-07 18:07

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_newpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='newpost',
            name='likes',
            field=models.ManyToManyField(related_name='posts_liked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='newpost',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]