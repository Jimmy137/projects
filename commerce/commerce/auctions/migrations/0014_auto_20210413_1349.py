# Generated by Django 3.1.6 on 2021-04-13 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_comment_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name']},
        ),
    ]