# Generated by Django 3.1.3 on 2020-11-17 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0013_auto_20201031_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='membermodel',
            name='reserve2',
            field=models.BooleanField(default=False),
        ),
    ]
