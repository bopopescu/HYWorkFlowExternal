# Generated by Django 3.0.4 on 2020-04-05 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchasing', '0025_purchaseorder_discount_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='document_number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Doc. No.'),
        ),
        migrations.AlterField(
            model_name='purchaseorderattachment',
            name='attachment_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='purchaseordercomparison2attachment',
            name='attachment_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='purchaseordercomparison3attachment',
            name='attachment_date',
            field=models.DateField(),
        ),
    ]