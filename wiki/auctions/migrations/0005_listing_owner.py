# Generated by Django 3.1.2 on 2020-11-02 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_closebid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='owner',
            field=models.CharField(default='', max_length=34),
        ),
    ]