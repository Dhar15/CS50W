# Generated by Django 3.1.2 on 2020-11-02 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
