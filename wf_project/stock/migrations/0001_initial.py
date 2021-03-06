# Generated by Django 3.0.3 on 2020-04-30 08:34

import ckeditor_uploader.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import stock.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administration', '0082_auto_20200429_0207'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Inventory', '0007_auto_20200327_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockAdjustment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.IntegerField(default=1)),
                ('document_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Document No')),
                ('submit_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('attention', models.CharField(max_length=250)),
                ('reference', models.CharField(blank=True, max_length=100, null=True)),
                ('remarks', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.CompanyMaintenance', verbose_name='Company')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.DepartmentMaintenance', verbose_name='Department')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.LocationMaintenance', verbose_name='Location')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.ProjectMaintenance', verbose_name='Project')),
                ('status', models.ForeignKey(blank=True, default=stock.models.stock_adjustment_default_status, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.StatusMaintenance', verbose_name='Status')),
                ('submit_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('transaction_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.TransactiontypeMaintenance', verbose_name='Trans. Type')),
            ],
            options={
                'verbose_name': 'Stock Adjustment',
                'verbose_name_plural': 'Stock Adjustment',
            },
        ),
        migrations.CreateModel(
            name='StockIssuing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.IntegerField(default=1)),
                ('document_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Document No')),
                ('delivery_address', models.CharField(blank=True, max_length=250, null=True)),
                ('submit_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('attention', models.CharField(max_length=250)),
                ('reference', models.CharField(blank=True, max_length=100, null=True)),
                ('remarks', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.CompanyMaintenance', verbose_name='Company')),
                ('delivery_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stocktransferdeliveryto', to='administration.CompanyMaintenance', verbose_name='Delivery Address')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.DepartmentMaintenance', verbose_name='Department')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.LocationMaintenance', verbose_name='Location')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.ProjectMaintenance', verbose_name='Project')),
                ('status', models.ForeignKey(blank=True, default=stock.models.stock_issuing_default_status, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.StatusMaintenance', verbose_name='Status')),
                ('submit_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('transaction_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.TransactiontypeMaintenance', verbose_name='Trans. Type')),
            ],
            options={
                'verbose_name': 'Stock Issuing',
                'verbose_name_plural': 'Stock Issuing',
            },
        ),
        migrations.CreateModel(
            name='StockTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.IntegerField(default=1)),
                ('document_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Document No')),
                ('submit_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('attention', models.CharField(max_length=250)),
                ('reference', models.CharField(blank=True, max_length=100, null=True)),
                ('remarks', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.CompanyMaintenance', verbose_name='Company')),
                ('from_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stocktransferfromlocation', to='administration.LocationMaintenance', verbose_name='From Location')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.ProjectMaintenance', verbose_name='Project')),
                ('status', models.ForeignKey(blank=True, default=stock.models.stock_transfer_default_status, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.StatusMaintenance', verbose_name='Status')),
                ('submit_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('to_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stocktransfertolocation', to='administration.LocationMaintenance', verbose_name='To Location')),
                ('transaction_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.TransactiontypeMaintenance', verbose_name='Trans. Type')),
            ],
            options={
                'verbose_name': 'Stock Transfer',
                'verbose_name_plural': 'Stock Transfer',
            },
        ),
        migrations.CreateModel(
            name='StockTransferDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_description', models.CharField(blank=True, max_length=250, null=True, verbose_name='Additional Description')),
                ('quantity', models.DecimalField(decimal_places=3, default=0.0, max_digits=15, verbose_name='Qty')),
                ('reason', models.CharField(blank=True, max_length=250, null=True)),
                ('remarks', models.CharField(blank=True, max_length=250, null=True)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Inventory.Item', verbose_name='Item')),
                ('stock_transfer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.StockTransfer')),
                ('uom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.UOMMaintenance', verbose_name='UOM')),
            ],
            options={
                'verbose_name': 'Stock Transfer Detail',
                'verbose_name_plural': 'Stock Transfer Detail',
            },
        ),
        migrations.CreateModel(
            name='StockTransferAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, null=True, upload_to=stock.models.stock_transfer_directory_path, verbose_name='File Name')),
                ('attachment_date', models.DateField()),
                ('stock_transfer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.StockTransfer')),
            ],
            options={
                'verbose_name': 'Stock Transfer Attachment',
            },
        ),
        migrations.CreateModel(
            name='StockIssuingDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_description', models.CharField(blank=True, max_length=250, null=True, verbose_name='Additional Description')),
                ('quantity', models.DecimalField(decimal_places=3, default=0.0, max_digits=15, verbose_name='Qty')),
                ('reason', models.CharField(blank=True, max_length=250, null=True)),
                ('remarks', models.CharField(blank=True, max_length=250, null=True)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Inventory.Item', verbose_name='Item')),
                ('stock_issuing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.StockIssuing')),
                ('uom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.UOMMaintenance', verbose_name='UOM')),
            ],
            options={
                'verbose_name': 'Stock Issuing Detail',
                'verbose_name_plural': 'Stock Issuing Detail',
            },
        ),
        migrations.CreateModel(
            name='StockIssuingAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, null=True, upload_to=stock.models.stock_issuing_directory_path, verbose_name='File Name')),
                ('attachment_date', models.DateField()),
                ('stock_issuing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.StockIssuing')),
            ],
            options={
                'verbose_name': 'Stock Issuing Attachment',
            },
        ),
        migrations.CreateModel(
            name='StockAdjustmentDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_description', models.CharField(blank=True, max_length=250, null=True, verbose_name='Additional Description')),
                ('quantity', models.DecimalField(decimal_places=3, default=0.0, max_digits=15, verbose_name='Qty')),
                ('reason', models.CharField(blank=True, max_length=250, null=True)),
                ('remarks', models.CharField(blank=True, max_length=250, null=True)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Inventory.Item', verbose_name='Item')),
                ('stock_adjustment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.StockAdjustment')),
                ('uom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.UOMMaintenance', verbose_name='UOM')),
            ],
            options={
                'verbose_name': 'Stock Adjustment Detail',
                'verbose_name_plural': 'Stock Adjustment Detail',
            },
        ),
        migrations.CreateModel(
            name='StockAdjustmentAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, null=True, upload_to=stock.models.stock_adjustment_directory_path, verbose_name='File Name')),
                ('attachment_date', models.DateField()),
                ('stock_adjustment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stock.StockAdjustment')),
            ],
            options={
                'verbose_name': 'Stock Adjustment Attachment',
            },
        ),
        migrations.CreateModel(
            name='ItemMovement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_pk', models.IntegerField()),
                ('stock_in', models.IntegerField()),
                ('stock_out', models.IntegerField()),
                ('document_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.DocumentTypeMaintenance', verbose_name='Document Type')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Inventory.Item', verbose_name='Item')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.LocationMaintenance', verbose_name='Location')),
            ],
        ),
    ]
