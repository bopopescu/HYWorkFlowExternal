# Generated by Django 3.0.3 on 2020-03-28 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0051_remove_currencymaintenance_country'),
        ('payment', '0006_auto_20200326_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrequest',
            name='employee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='administration.EmployeeMaintenance', verbose_name='Vendor'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.CompanyMaintenance', verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.CurrencyMaintenance', verbose_name='Currency'),
        ),
    ]