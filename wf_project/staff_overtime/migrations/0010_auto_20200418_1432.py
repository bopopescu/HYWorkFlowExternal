# Generated by Django 3.0.3 on 2020-04-18 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_overtime', '0009_auto_20200418_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffot',
            name='total_ot_rate',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=8, null=True),
        ),
    ]
