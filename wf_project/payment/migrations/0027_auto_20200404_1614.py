# Generated by Django 3.0.3 on 2020-04-04 08:14

import datetime
from django.db import migrations, models
import django.db.models.deletion
import payment.models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0062_drawerusermaintenance'),
        ('payment', '0026_auto_20200402_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrequest',
            name='status',
            field=models.ForeignKey(blank=True, default=payment.models.default_status, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.StatusMaintenance', verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='submit_date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
    ]
