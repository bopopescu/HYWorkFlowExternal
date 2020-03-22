# Generated by Django 3.0.3 on 2020-03-20 04:16

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0026_auto_20200311_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branchmaintenance',
            name='created_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='branchmaintenance',
            name='modified_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='companymaintenance',
            name='created_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='companymaintenance',
            name='modified_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='countrymaintenance',
            name='created_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='countrymaintenance',
            name='modified_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='currencymaintenance',
            name='created_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='currencymaintenance',
            name='modified_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='documenttypemaintenance',
            name='created_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='documenttypemaintenance',
            name='modified_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='employeebranchmaintenance',
            name='created_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='employeebranchmaintenance',
            name='modified_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='employeedepartmentmaintenance',
            name='created_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='employeedepartmentmaintenance',
            name='modified_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='employeegroupmaintenance',
            name='created_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='employeegroupmaintenance',
            name='modified_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='employeepositionmaintenance',
            name='created_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='employeepositionmaintenance',
            name='modified_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='employeeprojectmaintenance',
            name='created_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='employeeprojectmaintenance',
            name='modified_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='itemclassesmaintenance',
            name='created_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='itemclassesmaintenance',
            name='modified_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='itemgroupsmaintenance',
            name='created_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='itemgroupsmaintenance',
            name='modified_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='itemgroupsmaintenance',
            name='parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.ItemGroupsMaintenance', verbose_name='Parent Group'),
        ),
        migrations.AlterField(
            model_name='locationmaintenance',
            name='created_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='locationmaintenance',
            name='modified_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='projectmaintenance',
            name='effect_end_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='projectmaintenance',
            name='effect_start_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='regionmaintenance',
            name='created_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='regionmaintenance',
            name='modified_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='taxmaintenance',
            name='created_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='taxmaintenance',
            name='modified_timestamp',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
