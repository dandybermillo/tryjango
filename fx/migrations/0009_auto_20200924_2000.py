# Generated by Django 3.0.3 on 2020-09-24 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0008_auto_20200924_1916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tradingmodel',
            name='cc_id',
        ),
        migrations.AddField(
            model_name='tradingmodel',
            name='customer_cc_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tradingmodel',
            name='seller_cc_id',
            field=models.IntegerField(default=0),
        ),
    ]
