# Generated by Django 3.0.3 on 2020-05-08 03:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_auto_20200506_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemmovement',
            name='submit_date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
    ]
