# Generated by Django 3.1.6 on 2021-04-11 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='photo',
            field=models.URLField(default='http://google.com'),
        ),
    ]