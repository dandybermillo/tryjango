# Generated by Django 3.1.3 on 2021-01-10 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0030_auto_20210110_0755'),
    ]

    operations = [
        migrations.AddField(
            model_name='joinmodel',
            name='gender',
            field=models.CharField(choices=[('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs')], default='Mr.', max_length=4),
        ),
    ]