# Generated by Django 3.0.3 on 2020-03-27 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0042_employeemaintenance_employee_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeemaintenance',
            name='employee_department',
        ),
    ]