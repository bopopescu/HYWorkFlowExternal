# Generated by Django 3.0.3 on 2020-03-31 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('human_resource', '0013_auto_20200331_1734'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staffjobrequirement',
            old_name='staff_recruiment',
            new_name='staff_recruitment',
        ),
        migrations.RenameField(
            model_name='staffjobresponsibilities',
            old_name='staff_recruiment',
            new_name='staff_recruitment',
        ),
    ]
