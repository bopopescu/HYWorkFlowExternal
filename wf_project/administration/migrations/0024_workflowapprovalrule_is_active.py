# Generated by Django 3.0.3 on 2020-03-11 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0023_auto_20200311_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflowapprovalrule',
            name='is_active',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
