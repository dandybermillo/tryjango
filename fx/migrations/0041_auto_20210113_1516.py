# Generated by Django 3.1.3 on 2021-01-13 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0040_auto_20210112_0606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venturemodel',
            name='customer_source_id',
        ),
        migrations.RemoveField(
            model_name='venturemodel',
            name='seller',
        ),
        migrations.RemoveField(
            model_name='venturemodel',
            name='seller_cc_id',
        ),
        migrations.RemoveField(
            model_name='venturemodel',
            name='seller_source_id',
        ),
    ]