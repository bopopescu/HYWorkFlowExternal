# Generated by Django 3.0.3 on 2020-05-20 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0084_auto_20200514_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyaddressdetail',
            name='default',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companycontactdetail',
            name='default',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendoraddressdetail',
            name='default',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendorcontactdetail',
            name='default',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
