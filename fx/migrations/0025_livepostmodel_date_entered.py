# Generated by Django 3.1.3 on 2021-01-05 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0024_loadmodel_source_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='livepostmodel',
            name='date_entered',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]