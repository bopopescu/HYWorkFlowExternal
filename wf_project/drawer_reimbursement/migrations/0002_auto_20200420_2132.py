# Generated by Django 3.0.5 on 2020-04-20 13:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0072_auto_20200420_2112'),
        ('approval', '0008_auto_20200409_1247'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drawer_reimbursement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReimbursementRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('submit_date', models.DateField(default=datetime.date.today)),
                ('description', models.CharField(max_length=300)),
                ('document_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Document No')),
                ('approval', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='approval.ApprovalItem', verbose_name='Approval')),
                ('drawer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.DrawerMaintenance', verbose_name='Drawer')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.StatusMaintenance', verbose_name='Status')),
                ('submit_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='AdvanceRefund',
        ),
    ]