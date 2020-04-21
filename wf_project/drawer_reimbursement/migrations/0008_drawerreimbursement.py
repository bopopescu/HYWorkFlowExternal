# Generated by Django 3.0.5 on 2020-04-21 05:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administration', '0074_merge_20200421_1216'),
        ('drawer_reimbursement', '0007_auto_20200421_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrawerReimbursement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_reimburse', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reimbursed_date', models.DateField(auto_now_add=True)),
                ('drawer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.DrawerMaintenance', verbose_name='Drawer Maintenance')),
                ('reimbursed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reimbursement_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='drawer_reimbursement.ReimbursementRequest', verbose_name='Reimbursement Request')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.StatusMaintenance')),
            ],
        ),
    ]
