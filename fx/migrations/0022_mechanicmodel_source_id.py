# Generated by Django 3.1.3 on 2021-01-04 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0021_auto_20210102_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechanicmodel',
            name='source_id',
            field=models.IntegerField(default=0),
        ),
    ]