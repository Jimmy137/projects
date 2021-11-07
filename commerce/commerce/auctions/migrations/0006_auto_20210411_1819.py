# Generated by Django 3.1.6 on 2021-04-11 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210411_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(blank=True, default=4, on_delete=django.db.models.deletion.PROTECT, related_name='listings', to='auctions.category'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='photo',
            field=models.URLField(blank=True, default='http://google.com', null=True),
        ),
    ]
