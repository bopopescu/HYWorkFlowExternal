# Generated by Django 3.0.3 on 2020-05-15 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilityapprovalitem',
            name='approval_code',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Approval Code'),
        ),
        migrations.AddField(
            model_name='utilityapprovalitem',
            name='approved_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
