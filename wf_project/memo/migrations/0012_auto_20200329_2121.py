# Generated by Django 3.0.3 on 2020-03-29 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import memo.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('memo', '0011_merge_20200328_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='memo',
            name='submit_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='memo',
            name='revision',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='memoattachment',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to=memo.models.documenttype_directory_path, verbose_name='File Name'),
        ),
    ]