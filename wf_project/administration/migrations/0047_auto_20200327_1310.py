# Generated by Django 3.0.3 on 2020-03-27 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0046_auto_20200327_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendormaindata',
            name='is_qualified',
            field=models.BooleanField(),
        ),
    ]
