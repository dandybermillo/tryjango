# Generated by Django 3.1.3 on 2020-11-20 02:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0015_merge_20201120_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membermodel',
            name='reserve2',
        ),
    ]
