# Generated by Django 3.0.3 on 2020-03-25 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memo', '0006_auto_20200326_0313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memo',
            name='revision',
            field=models.IntegerField(default=0, max_length=100),
        ),
    ]
