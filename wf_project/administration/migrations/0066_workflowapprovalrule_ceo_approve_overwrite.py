# Generated by Django 3.0.4 on 2020-04-04 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0065_auto_20200404_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflowapprovalrule',
            name='ceo_approve_overwrite',
            field=models.BooleanField(default=False, verbose_name='CEO Approval Overwrite'),
            preserve_default=False,
        ),
    ]
