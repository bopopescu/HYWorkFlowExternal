# Generated by Django 3.0.4 on 2020-04-04 17:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_type', models.CharField(max_length=5)),
                ('description', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
                ('created_by', models.CharField(max_length=120)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modify_by', models.CharField(max_length=120)),
                ('modify_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('is_deleted', models.BooleanField(default=False, null=True)),
                ('delete_by', models.CharField(max_length=120)),
                ('delete_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'verbose_name_plural': 'AssetCategories',
            },
        ),
        migrations.CreateModel(
            name='AssetMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_number', models.CharField(max_length=35)),
                ('description', models.CharField(max_length=150)),
                ('acquisition_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('floor_plan_ref', models.CharField(max_length=50)),
                ('trustees', models.CharField(max_length=50)),
                ('cost_value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('net_book_value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('last_trn_date', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('current_trn_date', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('last_py_trn_date', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('last_pm_trn_date', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('disposal_date', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('proceeds_on_disposal', models.DecimalField(decimal_places=2, max_digits=8)),
                ('historical_cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('active_lifetime', models.DecimalField(decimal_places=2, max_digits=8)),
                ('active_res_value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tax_cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('current_tax_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('status', models.BooleanField(default=True)),
                ('remark', models.CharField(max_length=300)),
                ('created_by', models.CharField(blank=True, max_length=120, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modify_by', models.CharField(blank=True, max_length=120, null=True)),
                ('modify_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('is_deleted', models.BooleanField(default=False, null=True)),
                ('delete_by', models.CharField(blank=True, max_length=120, null=True)),
                ('delete_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('asset_category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixed_asset.AssetCategory')),
            ],
            options={
                'verbose_name_plural': 'AssetsMaster',
            },
        ),
        migrations.CreateModel(
            name='AssetType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_type', models.CharField(max_length=5)),
                ('description', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
                ('created_by', models.CharField(max_length=120)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modify_by', models.CharField(max_length=120)),
                ('modify_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('is_deleted', models.BooleanField(default=False, null=True)),
                ('delete_by', models.CharField(max_length=120)),
                ('delete_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'verbose_name_plural': 'AssetTypes',
            },
        ),
        migrations.CreateModel(
            name='ClassType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_type', models.CharField(max_length=5)),
                ('description', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
                ('created_by', models.CharField(max_length=120)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modify_by', models.CharField(max_length=120)),
                ('modify_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('is_deleted', models.BooleanField(default=False, null=True)),
                ('delete_by', models.CharField(max_length=120)),
                ('delete_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'verbose_name_plural': 'ClassTypes',
            },
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_code', models.CharField(max_length=5)),
                ('description', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
                ('created_by', models.CharField(max_length=120)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modify_by', models.CharField(max_length=120)),
                ('modify_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('is_deleted', models.BooleanField(default=False, null=True)),
                ('delete_by', models.CharField(max_length=120)),
                ('delete_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'verbose_name_plural': 'Taxes',
            },
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elapsed_months_py', models.DecimalField(decimal_places=2, max_digits=8)),
                ('elapsed_months_cy', models.DecimalField(decimal_places=2, max_digits=8)),
                ('elapsed_months_pm', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ac_opening_balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('additions', models.DecimalField(decimal_places=2, max_digits=8)),
                ('revaluations', models.DecimalField(decimal_places=2, max_digits=8)),
                ('disposals', models.DecimalField(decimal_places=2, max_digits=8)),
                ('impairment', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ac_closing_balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ad_opening_balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('depreciation_cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('depreciation_revaluation', models.DecimalField(decimal_places=2, max_digits=8)),
                ('depreciation_total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('acc_depr_revaluations', models.DecimalField(decimal_places=2, max_digits=8)),
                ('acc_depr_disposals', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ad_closing_balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('closing_carrying_value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('rr_opening_balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('revaluation_surplus', models.DecimalField(decimal_places=2, max_digits=8)),
                ('rr_depr_revaluation', models.DecimalField(decimal_places=2, max_digits=8)),
                ('rr_closing_balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('impairment_writeOffs', models.DecimalField(decimal_places=2, max_digits=8)),
                ('profit_Loss_on_disposal', models.DecimalField(decimal_places=2, max_digits=8)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('revaluation', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('hc_opening_balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('hc_ytd_movement', models.DecimalField(decimal_places=2, max_digits=8)),
                ('hc_closing_balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('hc_mtd_movement', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tv_opening_balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tv_ytd_movement', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tv_closing_balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tv_mtd_movement', models.DecimalField(decimal_places=2, max_digits=8)),
                ('dt_opening_balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('dt_ytd_movement', models.DecimalField(decimal_places=2, max_digits=8)),
                ('dt_closing_balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('dt_mtd_movement', models.DecimalField(decimal_places=2, max_digits=8)),
                ('status', models.BooleanField(default=True)),
                ('created_by', models.CharField(max_length=120)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modify_by', models.CharField(max_length=120)),
                ('modify_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('is_deleted', models.BooleanField(default=False, null=True)),
                ('delete_by', models.CharField(max_length=120)),
                ('delete_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('asset_master_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixed_asset.AssetMaster')),
            ],
            options={
                'verbose_name_plural': 'Statistics',
            },
        ),
        migrations.AddField(
            model_name='assetmaster',
            name='asset_type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixed_asset.AssetType'),
        ),
        migrations.AddField(
            model_name='assetmaster',
            name='class_type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixed_asset.ClassType'),
        ),
        migrations.AddField(
            model_name='assetmaster',
            name='tax_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fixed_asset.Tax'),
        ),
    ]
