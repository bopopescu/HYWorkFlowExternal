# Generated by Django 3.0.3 on 2020-03-30 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0058_merge_20200331_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxmaintenance',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Rate(%)'),
        ),
    ]
