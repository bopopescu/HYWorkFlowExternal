# Generated by Django 3.0.3 on 2020-04-18 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff_overtime', '0007_auto_20200415_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffot',
            name='total_ot_hours',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='staffot',
            name='total_ot_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]