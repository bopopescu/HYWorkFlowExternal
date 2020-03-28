# Generated by Django 3.0.3 on 2020-03-28 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0041_countrymaintenance_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='documenttypemaintenance',
            name='document_type_code',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documenttypemaintenance',
            name='running_number',
            field=models.IntegerField(default=1),
        ),
    ]
