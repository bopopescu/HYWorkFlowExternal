# Generated by Django 3.0.3 on 2020-04-02 04:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0062_drawerusermaintenance'),
        ('drawer_disbursement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='drawerdisbursement',
            name='drawer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.DrawerMaintenance', verbose_name='Drawer Maintenance'),
        ),
    ]
