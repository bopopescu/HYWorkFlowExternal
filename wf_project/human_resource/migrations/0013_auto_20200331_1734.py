# Generated by Django 3.0.3 on 2020-03-31 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('human_resource', '0012_auto_20200331_1659'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staffjobrequirement',
            old_name='staff_recruiment_id',
            new_name='staff_recruiment',
        ),
        migrations.RenameField(
            model_name='staffjobresponsibilities',
            old_name='staff_recruiment_id',
            new_name='staff_recruiment',
        ),
    ]