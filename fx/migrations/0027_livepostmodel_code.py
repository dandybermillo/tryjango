# Generated by Django 3.1.3 on 2021-01-09 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0026_auto_20210108_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='livepostmodel',
            name='code',
            field=models.PositiveIntegerField(choices=[(0, 'READY'), (1, 'NOT READY'), (2, 'COMPLETE')], default=1),
        ),
    ]
