# Generated by Django 3.0.3 on 2020-09-24 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0005_remove_tradingmodels_source_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TradingModels',
            new_name='TradingModel',
        ),
    ]
