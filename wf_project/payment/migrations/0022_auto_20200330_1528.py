# Generated by Django 3.0.3 on 2020-03-30 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0021_paymentrequest_submit_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrequestdetail',
            name='line_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
