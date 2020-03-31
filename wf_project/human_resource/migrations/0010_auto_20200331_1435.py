# Generated by Django 3.0.3 on 2020-03-31 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0060_auto_20200331_1432'),
        ('human_resource', '0009_auto_20200328_1644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staffrecruitmentrequest',
            name='hire_type',
        ),
        migrations.AddField(
            model_name='staffrecruitmentrequest',
            name='employment_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='administration.StaffemploymentTypeMaintenance', verbose_name='Employment Type'),
            preserve_default=False,
        ),
    ]