# Generated by Django 3.0.3 on 2020-03-28 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('human_resource', '0008_auto_20200328_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffrecruitmentrequest',
            name='revision',
            field=models.IntegerField(),
        ),
    ]
