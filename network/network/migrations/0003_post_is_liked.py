# Generated by Django 3.1.2 on 2020-11-28 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_follow_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_liked',
            field=models.BooleanField(default=False),
        ),
    ]