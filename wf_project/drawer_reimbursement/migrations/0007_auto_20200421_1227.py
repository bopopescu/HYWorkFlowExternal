# Generated by Django 3.0.5 on 2020-04-21 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drawer_reimbursement', '0006_auto_20200421_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reimbursementrequest',
            name='description',
            field=models.CharField(max_length=301),
        ),
    ]