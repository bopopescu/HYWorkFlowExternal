# Generated by Django 3.0.4 on 2020-04-05 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memo', '0021_auto_20200403_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memoattachment',
            name='attachment_date',
            field=models.DateField(),
        ),
    ]
