# Generated by Django 3.0.5 on 2020-04-21 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval', '0008_auto_20200409_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvalitem',
            name='approval_code',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Approval Code'),
        ),
    ]
