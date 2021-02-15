# Generated by Django 3.1.3 on 2021-02-15 06:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeGeneratorModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_id', models.IntegerField(default=0)),
                ('code', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='IdRepositoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=8, null=True, unique=True)),
                ('counter', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ItemModels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('category', models.PositiveIntegerField(choices=[(0, 'PERSONAL_HYGIENE'), (1, 'CANNED GOODS'), (2, 'DRY GOODS'), (3, 'PRODUCE'), (4, 'OTHER')], default=4)),
                ('qty', models.PositiveIntegerField()),
                ('price', models.FloatField()),
                ('reg_price', models.FloatField()),
                ('product_id', models.CharField(blank=True, max_length=13)),
                ('img', models.ImageField(blank=True, null=True, upload_to='')),
                ('sku', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='JoinModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs')], default='Mr.', max_length=4)),
                ('name', models.CharField(max_length=124)),
                ('phone', models.CharField(blank=True, max_length=124, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('code', models.PositiveIntegerField(choices=[(0, 'WAITING FOR APPROVAL'), (1, 'APPROVED'), (2, 'PENDING'), (3, 'DELETED')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MemberModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs')], max_length=4)),
                ('firstname', models.CharField(max_length=50)),
                ('middlename', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('lastname', models.CharField(max_length=50)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('telephone', models.CharField(blank=True, max_length=100, null=True)),
                ('note', models.TextField(blank=True, max_length=400, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('reserve', models.BooleanField(default=False)),
                ('member_id', models.CharField(default='default', max_length=11, unique=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MessageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=124)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('message', models.CharField(max_length=300)),
                ('source_id', models.IntegerField(default=0)),
                ('served', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='NoteModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.IntegerField(default=0)),
                ('note', models.TextField(blank=True, help_text='Enter note when necessary. Thank you', max_length=300, null=True)),
                ('category', models.PositiveIntegerField(choices=[(0, 'REGULAR TRANSACTION'), (1, 'LOAN'), (2, 'GROCERY'), (3, 'PAYMENT'), (7, 'TRADING')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PendingLoanModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_id', models.IntegerField(default=0)),
                ('cc_loan', models.FloatField(default=0)),
                ('saving', models.FloatField(default=0)),
                ('percent', models.FloatField(default=0)),
                ('source_type', models.CharField(blank=True, default='C', max_length=1)),
                ('source_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Mr.', 'Mr.'), ('Ms.', 'Ms.'), ('Mrs.', 'Mrs')], default='Mr.', max_length=4)),
                ('source_id', models.IntegerField(default=0)),
                ('firstname', models.CharField(max_length=50)),
                ('middlename', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('lastname', models.CharField(max_length=50)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('telephone', models.CharField(blank=True, max_length=100, null=True)),
                ('note', models.TextField(blank=True, max_length=400, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SkillCategoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tmp_PasswordModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pwd', models.CharField(max_length=12)),
                ('qrcode_pwd', models.CharField(default='', max_length=12)),
                ('member_id', models.IntegerField()),
                ('date_entry', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tmp_UsernameModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('code_counter', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='tmpVariables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_loan', models.FloatField(default=300, verbose_name='Max loan allowrd')),
            ],
        ),
        migrations.CreateModel(
            name='WalletModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
                ('date_entered', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('transaction_type', models.CharField(blank=True, choices=[('D', 'DEPOSIT'), ('W', 'WITHRAW')], max_length=1)),
                ('debit', models.FloatField(default=0, verbose_name='Amount to Cash Out')),
                ('credit', models.FloatField(default=0, verbose_name='Amount Cash In')),
                ('category', models.PositiveIntegerField(choices=[(0, 'REGULAR TRANSACTION'), (1, 'TRANSFER'), (2, 'GROCERY'), (5, 'LOAN'), (6, 'VENTURE'), (7, 'TRADING')], default=0)),
                ('source_id', models.IntegerField(default=0)),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='VentureWalletModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
                ('date_entered', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('transaction_type', models.CharField(blank=True, choices=[('D', 'DEPOSIT'), ('W', 'WITHRAW')], max_length=1)),
                ('debit', models.FloatField(default=0, verbose_name='Amount to Cash Out')),
                ('credit', models.FloatField(default=0, verbose_name='Amount Cash In')),
                ('category', models.PositiveIntegerField(choices=[(0, 'REGULAR TRANSACTION'), (1, 'TRANSFER'), (2, 'GROCERY'), (5, 'LOAN'), (6, 'VENTURE'), (7, 'TRADING')], default=0)),
                ('source_id', models.IntegerField(default=0)),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='VentureModel',
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
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Trading_Customer', to='fx.membermodel')),
                ('in_charge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='in_charge', to='fx.membermodel')),
            ],
        ),
        migrations.CreateModel(
            name='VentureCcModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('date_entered', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('transaction_type', models.CharField(blank=True, choices=[('D', 'DEPOSIT'), ('W', 'WITHRAW')], default='D', max_length=1)),
                ('debit', models.FloatField(default=0, verbose_name='Amount to Cash Out')),
                ('credit', models.FloatField(default=0, verbose_name='Amount to Cash In')),
                ('category', models.PositiveIntegerField(choices=[(0, 'REGULAR TRANSACTION'), (1, 'TRANSFER'), (2, 'GROCERY'), (3, 'SAVING_INTEREST'), (4, 'EARNED'), (5, 'LOAN')], default=0)),
                ('source_id', models.IntegerField(default=0)),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='UserPreferenceModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('financial_transaction', models.PositiveIntegerField(default=5)),
                ('cash_transfer_nos_of_row', models.PositiveIntegerField(default=5)),
                ('search_member', models.PositiveIntegerField(default=5)),
                ('search_receiver', models.PositiveIntegerField(default=5)),
                ('transfer_receiver', models.PositiveIntegerField(default=5)),
                ('transfer_history', models.PositiveIntegerField(default=5)),
                ('claim_transfer', models.PositiveIntegerField(default=5)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransferModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, default='W', max_length=1)),
                ('date_entered', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('code', models.PositiveIntegerField(default=0)),
                ('purpose', models.CharField(blank=True, max_length=100)),
                ('source_type', models.CharField(choices=[('W', 'WALLET'), ('C', 'CC'), ('S', 'SAVING')], default='W', max_length=1)),
                ('source_id', models.IntegerField(default=0)),
                ('date_accounted', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('flag', models.PositiveIntegerField(choices=[(0, 'UNACCEPTED'), (1, 'ACCEPTED'), (2, 'BEING_EDITED'), (3, 'DONE_EDITING')], default=0)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Cash_receiver', to='fx.membermodel')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Cash_sender', to='fx.membermodel')),
            ],
        ),
        migrations.CreateModel(
            name='TradingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(blank=True, choices=[('D', 'DEPOSIT'), ('W', 'WITHRAW')], max_length=1)),
                ('role_type', models.CharField(choices=[('B', 'BUYER'), ('S', 'SELLER')], default='B', max_length=1)),
                ('category', models.PositiveIntegerField(choices=[(0, 'REGULAR TRANSACTION'), (1, 'TRANSFER'), (2, 'GROCERY'), (5, 'LOAN'), (7, 'TRADE')], default=7)),
                ('amount', models.FloatField(verbose_name='AMOUNT')),
                ('customer_source_id', models.IntegerField(default=0)),
                ('seller_source_id', models.IntegerField(default=0)),
                ('cc', models.FloatField(default=0, verbose_name='CC')),
                ('percent', models.FloatField(default=95)),
                ('source_type', models.CharField(choices=[('W', 'WALLET ACCOUNT'), ('K', 'CASH'), ('S', 'SAVINGS ACCOUNT')], default='K', max_length=1)),
                ('customer_cc_id', models.IntegerField(default=0)),
                ('seller_cc_id', models.IntegerField(default=0)),
                ('date_entered', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('flag', models.PositiveIntegerField(choices=[(0, 'UNACCEPTED'), (1, 'ACCEPTED'), (2, 'BEING_EDITED'), (3, 'DONE_EDITING')], default=0)),
                ('note_id', models.IntegerField(default=0)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Customer', to='fx.membermodel')),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Seller', to='fx.membermodel')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMemberModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.skillcategorymodel')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
        ),
        migrations.CreateModel(
            name='SavingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('date_entered', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('transaction_type', models.CharField(blank=True, choices=[('D', 'DEPOSIT'), ('W', 'WITHRAW')], default='D', max_length=1)),
                ('debit', models.FloatField(default=0, verbose_name='Amount to Cash Out')),
                ('credit', models.FloatField(default=0, verbose_name='Amount to Cash In')),
                ('category', models.PositiveIntegerField(choices=[(1, 'TRANSFER'), (5, 'LOAN'), (6, 'PAYMENT')], default=0)),
                ('source_id', models.IntegerField(default=0)),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='RepairModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=124)),
                ('phone', models.CharField(max_length=124)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('description', models.CharField(max_length=300)),
                ('served', models.BooleanField(default=False)),
                ('date_entered', models.DateField(auto_now_add=True, null=True)),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalLoanModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cc_loan', models.FloatField(default=0, verbose_name='Community Coin(CC)')),
                ('saving', models.FloatField(default=0, verbose_name='Saving(Deposit)')),
                ('percent', models.PositiveIntegerField(default=0)),
                ('source_type', models.CharField(blank=True, default='C', max_length=1)),
                ('source_id', models.IntegerField(default=0)),
                ('cc_id', models.IntegerField(default=0)),
                ('saving_id', models.IntegerField(default=0)),
                ('date_entered', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('note_id', models.IntegerField(default=0)),
                ('flag', models.PositiveIntegerField(choices=[(0, 'UNACCEPTED'), (1, 'ACCEPTED'), (2, 'BEING_EDITED'), (3, 'DONE_EDITING')], default=0)),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PaymentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_entered', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('transaction_type', models.CharField(blank=True, choices=[('D', 'DEPOSIT'), ('W', 'WITHRAW')], default='D', max_length=1)),
                ('debit', models.FloatField(default=0, verbose_name='Amount')),
                ('credit', models.FloatField(default=0, verbose_name='Amount to Cash In')),
                ('category', models.PositiveIntegerField(choices=[(5, 'LOAN'), (6, 'PAYMENT')], default=0)),
                ('source_id', models.IntegerField(default=0)),
                ('source_type', models.CharField(blank=True, default='C', max_length=1)),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='NonCashTransferModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, default='W', max_length=1)),
                ('date_entered', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('code', models.PositiveIntegerField(default=0)),
                ('purpose', models.CharField(blank=True, max_length=100)),
                ('source_type', models.PositiveIntegerField(choices=[(1, 'WALLET'), (2, 'CC'), (3, 'SAVING')], default=1)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Non_Cash_receiver', to='fx.membermodel')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Non_Cash_sender', to='fx.membermodel')),
            ],
        ),
        migrations.CreateModel(
            name='MechanicModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=124)),
                ('phone', models.CharField(max_length=124)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.CharField(max_length=300)),
                ('category', models.PositiveIntegerField(choices=[(0, 'AUTO MECHANIC'), (1, 'GENERAL MECHANiC')], default=0)),
                ('description', models.CharField(max_length=300)),
                ('served', models.BooleanField(default=False)),
                ('date_entered', models.DateField(auto_now_add=True, null=True)),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
        ),
        migrations.CreateModel(
            name='LoanSummaryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_entered', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('max_loan', models.FloatField(default=300, verbose_name='Max Loan')),
                ('percent', models.PositiveIntegerField(default=25)),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
        ),
        migrations.CreateModel(
            name='LoadModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=124)),
                ('phone', models.CharField(max_length=124)),
                ('carrier', models.PositiveIntegerField(choices=[(0, 'SMART'), (1, 'GLOBE'), (2, 'DITO'), (3, 'TALK N TEXT'), (4, 'SUN CELLULAR')], default=0)),
                ('email', models.EmailField(blank=True, max_length=250, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('amount', models.FloatField(default=0)),
                ('date_entered', models.DateField(auto_now_add=True, null=True)),
                ('served', models.BooleanField(default=False)),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
        ),
        migrations.CreateModel(
            name='LivePostModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('code', models.PositiveIntegerField(choices=[(0, 'WAITING FOR APPROVAL'), (2, 'APPROVED'), (1, 'NOT READY'), (3, 'READY FOR DISPOSAL'), (4, 'DELETED')], default=2)),
                ('remarks', models.CharField(default='In Progress', max_length=300)),
                ('category', models.PositiveIntegerField(choices=[(1, 'MOBILE TOP UP'), (2, 'COMPUTER REPAIR'), (3, 'MECHANIC'), (4, 'CONSTRUCTION'), (5, 'DELIVERY')], default=1)),
                ('date_entered', models.DateField(auto_now_add=True, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cus', to='fx.membermodel')),
                ('in_charge', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inc', to='fx.teammembermodel')),
            ],
        ),
        migrations.CreateModel(
            name='ItemSolds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=0)),
                ('amount', models.FloatField(default=0)),
                ('cm', models.FloatField(default=0)),
                ('price', models.FloatField(default=0)),
                ('transaction_id', models.PositiveIntegerField(default=0)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.itemmodels')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=124)),
                ('phone', models.CharField(blank=True, max_length=124, null=True)),
                ('address', models.CharField(max_length=300)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('recepient', models.CharField(max_length=124)),
                ('recepient_address', models.CharField(max_length=124)),
                ('recepient_phone', models.CharField(blank=True, max_length=124, null=True)),
                ('message', models.CharField(blank=True, max_length=300, null=True)),
                ('served', models.BooleanField(default=False)),
                ('date_entered', models.DateField(auto_now_add=True, null=True)),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
        ),
        migrations.CreateModel(
            name='dayTransactionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.PositiveIntegerField(choices=[(3, 'REGULAR TRANSACTION'), (0, 'PAYMENT'), (2, 'VENTURE'), (4, 'DEPOSIT'), (5, 'WITHRAWAL'), (6, 'GROCERY'), (7, 'SERVICES'), (1, 'LOAN PAYMENT')], default=1)),
                ('date_entered', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('source_type', models.IntegerField(choices=[(0, 'CASH'), (1, 'WALLET ACCOUNT'), (2, 'SAVING ACCOUNT')], default=0)),
                ('amount', models.FloatField(default=0)),
                ('source_id', models.IntegerField(default=0)),
                ('account_code', models.PositiveIntegerField(choices=[(1, 'SAVING ACCOUNT'), (2, 'WALLET ACCOUNT'), (3, 'CC ACCOUNT'), (4, 'VENTURE ACCOUNT'), (5, 'PAYMENT ACCOUNT')], default=1)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='venture_customer', to='fx.membermodel')),
                ('in_charge', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='venture_in_charge', to='fx.membermodel')),
            ],
        ),
        migrations.CreateModel(
            name='ConstructionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=124)),
                ('phone', models.CharField(max_length=124)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('category', models.PositiveIntegerField(choices=[(0, 'Worker'), (1, 'Materials'), (2, 'Mason'), (3, 'Forman')], default=0)),
                ('message', models.CharField(max_length=300)),
                ('served', models.BooleanField(default=False)),
                ('date_entered', models.DateField(auto_now_add=True, null=True)),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
        ),
        migrations.CreateModel(
            name='Change_Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change', models.FloatField(verbose_name='PHP')),
                ('destination_acct_id', models.IntegerField(default=0)),
                ('date_entered', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('destination_acct_code', models.CharField(blank=True, default='', max_length=1)),
                ('venture', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.venturemodel')),
            ],
        ),
        migrations.CreateModel(
            name='CcModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('date_entered', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('transaction_type', models.CharField(blank=True, choices=[('D', 'DEPOSIT'), ('W', 'WITHRAW')], default='D', max_length=1)),
                ('debit', models.FloatField(default=0, verbose_name='Amount to Cash Out')),
                ('credit', models.FloatField(default=0, verbose_name='Amount to Cash In')),
                ('category', models.PositiveIntegerField(choices=[(0, 'REGULAR TRANSACTION'), (1, 'TRANSFER'), (2, 'GROCERY'), (3, 'SAVING_INTEREST'), (4, 'EARNED'), (5, 'LOAN'), (6, 'VENTURE'), (7, 'TRADING')], default=0)),
                ('source_id', models.IntegerField(default=0)),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fx.membermodel')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
