# Generated by Django 3.0.3 on 2020-03-23 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0035_merge_20200323_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='documenttypemaintenance',
            name='attachment_path',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
    ]