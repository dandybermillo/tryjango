# Generated by Django 3.0.3 on 2020-10-31 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0010_auto_20200927_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmp_passwordmodel',
            name='qrcode_pwd',
            field=models.CharField(default='', max_length=4),
        ),
    ]
