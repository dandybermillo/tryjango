# Generated by Django 3.1.3 on 2021-01-26 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0050_auto_20210126_1552'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loadmodel',
            old_name='source_id',
            new_name='source',
        ),
    ]