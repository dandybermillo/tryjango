# Generated by Django 3.1.3 on 2021-01-26 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0049_auto_20210126_0453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loadmodel',
            name='source_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel'),
        ),
    ]