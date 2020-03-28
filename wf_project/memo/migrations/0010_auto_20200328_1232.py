# Generated by Django 3.0.3 on 2020-03-28 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memo', '0009_memo_approval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memoattachment',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='File Name'),
        ),
        migrations.AlterField(
            model_name='memoattachment',
            name='memo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='memo.Memo', verbose_name='Memo'),
        ),
    ]
