# Generated by Django 3.0.3 on 2020-03-11 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0020_merge_20200311_0943'),
        ('purchasing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestForQuotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.CharField(max_length=100)),
                ('document_number', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=1)),
                ('submit_date', models.DateField()),
                ('doc_date', models.DateField()),
                ('subject', models.CharField(max_length=250)),
                ('reference', models.CharField(max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.CompanyMaintenance', verbose_name='Company')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.ProjectMaintenance', verbose_name='Project')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.EmployeeMaintenance', verbose_name='Requester')),
            ],
            options={
                'verbose_name': 'Request For Quotation',
            },
        ),
        migrations.CreateModel(
            name='PurchaseQuotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.CharField(max_length=100)),
                ('document_number', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=1)),
                ('submit_date', models.DateField()),
                ('subject', models.CharField(max_length=250)),
                ('reference', models.CharField(max_length=100)),
                ('recommended', models.BooleanField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.CompanyMaintenance', verbose_name='Company')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.DepartmentMaintenance', verbose_name='Department')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.ProjectMaintenance', verbose_name='Project')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.EmployeeMaintenance', verbose_name='Vendor')),
            ],
            options={
                'verbose_name': 'Purchase Quotation',
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.CharField(max_length=100)),
                ('document_number', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=1)),
                ('submit_date', models.DateField()),
                ('subject', models.CharField(max_length=250)),
                ('reference', models.CharField(max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.CompanyMaintenance', verbose_name='Company')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.ProjectMaintenance', verbose_name='Project')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.EmployeeMaintenance', verbose_name='Vendor')),
            ],
            options={
                'verbose_name': 'Purchase Order',
            },
        ),
        migrations.CreateModel(
            name='GoodsReceiptNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.CharField(max_length=100)),
                ('document_number', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=1)),
                ('submit_date', models.DateField()),
                ('subject', models.CharField(max_length=250)),
                ('reference', models.CharField(max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.CompanyMaintenance', verbose_name='Company')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.CurrencyMaintenance', verbose_name='Currency')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.ProjectMaintenance', verbose_name='Project')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.EmployeeMaintenance', verbose_name='Vendor')),
            ],
            options={
                'verbose_name': 'Goods Receipt Note',
            },
        ),
    ]
