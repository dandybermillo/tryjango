# Generated by Django 3.1.3 on 2020-12-27 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0049_auto_20201227_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverymodel',
            name='phone',
            field=models.CharField(blank=True, max_length=124, null=True),
        ),
        migrations.AlterField(
            model_name='joinmodel',
            name='phone',
            field=models.CharField(blank=True, max_length=124, null=True),
        ),
    ]
