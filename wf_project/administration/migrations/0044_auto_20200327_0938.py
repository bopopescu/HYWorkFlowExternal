# Generated by Django 3.0.3 on 2020-03-27 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0043_remove_employeemaintenance_employee_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeemaintenance',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='employeemaintenance',
            name='dob',
            field=models.DateField(blank=True, null=True, verbose_name='Date of Birth'),
        ),
    ]