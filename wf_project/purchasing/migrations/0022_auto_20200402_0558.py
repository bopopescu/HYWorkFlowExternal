# Generated by Django 3.0.4 on 2020-04-02 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0062_drawerusermaintenance'),
        ('purchasing', '0021_auto_20200401_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='document_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.ProjectMaintenance', verbose_name='Project'),
        ),
    ]
