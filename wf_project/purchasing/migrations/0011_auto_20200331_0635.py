# Generated by Django 3.0.3 on 2020-03-30 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('approval', '0004_auto_20200331_0251'),
        ('administration', '0059_auto_20200331_0248'),
        ('purchasing', '0010_purchaseorder_submit_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='transaction_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.TransactiontypeMaintenance', verbose_name='Transaction Type'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='approval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='approval.ApprovalItem', verbose_name='Approval'),
        ),
    ]