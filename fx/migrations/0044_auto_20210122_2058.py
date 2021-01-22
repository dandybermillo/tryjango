# Generated by Django 3.1.3 on 2021-01-22 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0043_auto_20210118_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livepostmodel',
            name='code',
            field=models.PositiveIntegerField(choices=[(0, 'WAITING FOR APPROVAL'), (2, 'APPROVED'), (1, 'NOT READY'), (3, 'READY FOR DISPOSAL'), (4, 'DELETED')], default=2),
        ),
    ]