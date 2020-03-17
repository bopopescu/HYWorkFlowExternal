# Generated by Django 3.0.3 on 2020-03-17 04:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0002_auto_20200225_1558'),
        ('purchasing', '0003_auto_20200317_0813'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaserequest',
            name='attachment',
            field=models.FileField(default='', upload_to='', verbose_name='File Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaserequest',
            name='attachment_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaserequest',
            name='remarks',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchaserequest',
            name='sub_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='PurchaseRequestDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250, verbose_name='Additional Description')),
                ('eta', models.DateTimeField(verbose_name='ETA Date')),
                ('quantity', models.IntegerField(verbose_name='Qty')),
                ('amount', models.IntegerField()),
                ('remark', models.CharField(max_length=250)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventory.Item', verbose_name='Item')),
                ('pr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchasing.PurchaseRequest')),
            ],
            options={
                'verbose_name': 'Detail',
            },
        ),
        migrations.CreateModel(
            name='PurchaseRequestCC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('email', models.CharField(max_length=250, verbose_name='Email')),
                ('pr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchasing.PurchaseRequest')),
            ],
            options={
                'verbose_name': 'CC',
            },
        ),
        migrations.CreateModel(
            name='PurchaseRequestAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='To')),
                ('address', models.CharField(max_length=250, verbose_name='Address')),
                ('pr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchasing.PurchaseRequest')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
    ]
