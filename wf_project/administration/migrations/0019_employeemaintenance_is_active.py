# Generated by Django 3.0.3 on 2020-03-10 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0018_auto_20200310_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeemaintenance',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
