# Generated by Django 3.0.3 on 2020-03-23 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0036_documenttypemaintenance_attachment_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeemaintenance',
            name='employee_group',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='administration.EmployeeGroupMaintenance', verbose_name='Employee Group'),
        ),
    ]
