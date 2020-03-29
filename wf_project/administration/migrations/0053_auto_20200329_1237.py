# Generated by Django 3.0.3 on 2020-03-29 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0052_merge_20200329_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflowapprovalrulegroupmaintenance',
            name='approval_group',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='administration.WorkflowApprovalGroup', verbose_name='Approval Group'),
        ),
        migrations.AlterField(
            model_name='workflowapprovalrulegroupmaintenance',
            name='next_condition',
            field=models.CharField(choices=[('And', 'And'), ('Or', 'Or')], max_length=15, null=True),
        ),
    ]
