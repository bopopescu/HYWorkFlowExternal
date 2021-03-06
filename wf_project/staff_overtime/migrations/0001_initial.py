# Generated by Django 3.0.3 on 2020-04-13 02:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administration', '0069_workflowapprovalrulegroupmaintenance_submitter_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffOT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revision', models.IntegerField()),
                ('document_number', models.CharField(max_length=100)),
                ('submit_date', models.DateField(default=datetime.date.today)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.CompanyMaintenance', verbose_name='Company')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.DepartmentMaintenance', verbose_name='Department')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.EmployeeMaintenance', verbose_name='Employee')),
                ('employee_position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.EmployeePositionMaintenance', verbose_name='Position')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.ProjectMaintenance', verbose_name='Project')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.StatusMaintenance', verbose_name='Status')),
                ('transaction_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.TransactiontypeMaintenance', verbose_name='Trans Type.')),
            ],
            options={
                'verbose_name': 'Staff OT',
            },
        ),
        migrations.CreateModel(
            name='StaffOTDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ot_date', models.DateField()),
                ('ot_time_in', models.TimeField()),
                ('ot_time_ot', models.TimeField()),
                ('meal_allowance', models.BooleanField()),
                ('remark', models.CharField(max_length=200)),
                ('staff_ot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staff_overtime.StaffOT', verbose_name='Staff OT')),
            ],
        ),
    ]
