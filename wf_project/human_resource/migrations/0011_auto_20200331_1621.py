# Generated by Django 3.0.3 on 2020-03-31 08:21

from django.db import migrations, models
import django.db.models.deletion
import human_resource.models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0061_staffpositiongrademaintenance'),
        ('human_resource', '0010_auto_20200331_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffrecruitmentrequest',
            name='position_grade',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='administration.StaffPositionGradeMaintenance', verbose_name='Position Grade'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='staffrecruitmentrequest',
            name='document_number',
            field=models.CharField(max_length=100, verbose_name='Document No.'),
        ),
    ]
