# Generated by Django 3.0.3 on 2020-03-28 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0050_staffhiretypemaintenance_staffpositiontitlemaintenance_utiliyaccounttypemaintenance'),
        ('human_resource', '0004_auto_20200328_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffrecruitmentrequest',
            name='hire_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.StaffHireTypeMaintenance', verbose_name='Hire Type'),
        ),
        migrations.AlterField(
            model_name='staffrecruitmentrequest',
            name='position_title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.StaffPositionTitleMaintenance', verbose_name='Position Title'),
        ),
    ]