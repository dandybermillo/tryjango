# Generated by Django 3.1.3 on 2021-01-01 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0014_auto_20210101_0503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membermodel',
            name='middlename',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profilemodel',
            name='middlename',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
