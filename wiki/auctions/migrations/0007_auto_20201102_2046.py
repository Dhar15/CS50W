# Generated by Django 3.1.2 on 2020-11-02 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20201102_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.CharField(default='', max_length=34),
        ),
        migrations.AlterField(
            model_name='listing',
            name='owner',
            field=models.CharField(max_length=34),
        ),
    ]