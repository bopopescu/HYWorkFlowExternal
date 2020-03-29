# Generated by Django 3.0.3 on 2020-03-29 16:35

from django.db import migrations, models
import memo.models


class Migration(migrations.Migration):

    dependencies = [
        ('memo', '0012_auto_20200329_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memo',
            name='document_number',
            field=models.CharField(blank=True, default=memo.models.documenttype_document_number, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='memo',
            name='status',
            field=models.CharField(blank=True, default='D', max_length=1, null=True),
        ),
    ]
