# Generated by Django 3.0.3 on 2020-02-25 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0004_itemgroupsmaintenance_parent_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyMaintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_code', models.CharField(max_length=100)),
                ('currency_name', models.CharField(max_length=250)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentTypeMaintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type_code', models.CharField(max_length=100)),
                ('document_type_name', models.CharField(max_length=250)),
                ('is_active', models.BooleanField()),
                ('created_by', models.CharField(max_length=100)),
                ('created_timestamp', models.DateField()),
                ('modified_by', models.CharField(max_length=100)),
                ('modified_timestamp', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='projectmaintenance',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='administration.CompanyMaintenance', verbose_name='Company Name'),
        ),
        migrations.AddField(
            model_name='usermaintenance',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='administration.CompanyMaintenance', verbose_name='Company Name'),
        ),
        migrations.AddField(
            model_name='workflowinstance',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='administration.CompanyMaintenance', verbose_name='Company Name'),
        ),
        migrations.AddField(
            model_name='companymaintenance',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='administration.CurrencyMaintenance', verbose_name='Currency'),
        ),
        migrations.AddField(
            model_name='statusmaintenance',
            name='document_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='administration.DocumentTypeMaintenance', verbose_name='Document Type'),
        ),
        migrations.AddField(
            model_name='workflowinstance',
            name='document_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='administration.DocumentTypeMaintenance', verbose_name='Document Type'),
        ),
    ]
