# Generated by Django 3.0.3 on 2020-04-02 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0062_drawerusermaintenance'),
        ('memo', '0016_auto_20200402_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memo',
            name='document_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='memo',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.ProjectMaintenance', verbose_name='Project'),
        ),
    ]
