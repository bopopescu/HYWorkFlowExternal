# Generated by Django 3.0.3 on 2020-03-30 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0022_auto_20200330_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrequestdetail',
            name='line_taxamount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]