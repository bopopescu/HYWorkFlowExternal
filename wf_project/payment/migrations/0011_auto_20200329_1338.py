# Generated by Django 3.0.3 on 2020-03-29 05:38

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0010_auto_20200329_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrequest',
            name='remarks',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]