# Generated by Django 3.0.3 on 2020-03-10 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administration', '0014_auto_20200310_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorQualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.CharField(max_length=100)),
                ('document_number', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=1)),
                ('submit_date', models.DateField()),
                ('reference', models.CharField(max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.CompanyMaintenance', verbose_name='Company')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.DepartmentMaintenance', verbose_name='Department')),
                ('document_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.DocumentTypeMaintenance', verbose_name='Document Type')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.VendorMasterData', verbose_name='Vendor')),
            ],
            options={
                'verbose_name': 'Vendor Qualification',
                'verbose_name_plural': 'Vendor Qualifications',
            },
        ),
    ]
