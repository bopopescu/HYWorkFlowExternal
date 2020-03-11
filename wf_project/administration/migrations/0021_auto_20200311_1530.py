# Generated by Django 3.0.3 on 2020-03-11 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0020_merge_20200311_0943'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workflowapprovalrule',
            old_name='ApprovalLevel',
            new_name='approval_level',
        ),
        migrations.RenameField(
            model_name='workflowapprovalrule',
            old_name='Description',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='workflowapprovalrule',
            name='Condition',
        ),
        migrations.AddField(
            model_name='workflowapprovalrule',
            name='condition',
            field=models.CharField(choices=[('And', 'And'), ('Or', 'Or')], default=1, max_length=10, verbose_name='Condition'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workflowapprovalrule',
            name='document_amount_range',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Document Amount Range'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workflowapprovalrule',
            name='document_amount_range2',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workflowapprovalrule',
            name='no_of_groupa',
            field=models.IntegerField(default=1, verbose_name='No of Group A User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workflowapprovalrule',
            name='no_of_groupb',
            field=models.IntegerField(default=1, verbose_name='No of Group B User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workflowapprovalrule',
            name='supervisor_approve',
            field=models.BooleanField(default=True, verbose_name='Supervisor Approve?'),
            preserve_default=False,
        ),
    ]
