# Generated by Django 3.0.3 on 2020-04-05 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0065_employeecompanymaintenance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeecompanymaintenance',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.CompanyMaintenance', verbose_name='Company'),
        ),
    ]