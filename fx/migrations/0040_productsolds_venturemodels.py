# Generated by Django 3.1.3 on 2021-04-03 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fx', '0039_remove_productsold_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='VentureModels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(blank=True, choices=[('D', 'DEPOSIT'), ('W', 'WITHRAW')], max_length=1)),
                ('category', models.PositiveIntegerField(choices=[(0, 'REGULAR TRANSACTION'), (1, 'TRANSFER'), (2, 'GROCERY'), (5, 'LOAN'), (7, 'TRADE')], default=2)),
                ('amount', models.FloatField(verbose_name='AMOUNT (PHP)')),
                ('cc', models.FloatField(default=0, verbose_name='CO. MONEY')),
                ('percent', models.FloatField(default=95)),
                ('source_type', models.CharField(choices=[('W', 'WALLET ACCOUNT'), ('K', 'CASH'), ('S', 'SAVINGS ACCOUNT')], default='K', max_length=1)),
                ('customer_source_id', models.IntegerField(default=0)),
                ('customer_cc_id', models.IntegerField(default=0)),
                ('date_entered', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('flag', models.PositiveIntegerField(choices=[(0, 'UNACCEPTED'), (1, 'ACCEPTED'), (2, 'BEING_EDITED'), (3, 'DONE_EDITING')], default=0)),
                ('note_id', models.IntegerField(default=0)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Trading_Customers', to='fx.membermodel')),
                ('in_charge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='in_charges', to='fx.membermodel')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSolds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.FloatField(default=0)),
                ('amount', models.FloatField(default=0)),
                ('cm', models.FloatField(default=0)),
                ('price', models.FloatField(default=0)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('transaction_id', models.PositiveIntegerField(default=0)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.productmodel')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
        ),
    ]