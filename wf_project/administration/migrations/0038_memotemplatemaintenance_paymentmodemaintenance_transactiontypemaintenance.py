# Generated by Django 3.0.3 on 2020-03-24 07:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administration', '0037_employeemaintenance_employee_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactiontypeMaintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type_name', models.CharField(max_length=250)),
                ('is_active', models.BooleanField()),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modified_timestamp', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactiontypecreated_by_user', to=settings.AUTH_USER_MODEL)),
                ('document_type', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='administration.DocumentTypeMaintenance', verbose_name='Document Type')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactiontypemodified_by_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentmodeMaintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_mode_name', models.CharField(max_length=250)),
                ('is_active', models.BooleanField()),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modified_timestamp', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paymentmodecreated_by_user', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paymentmodemodified_by_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MemoTemplateMaintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memo_template_name', models.CharField(max_length=250, verbose_name='Memo Template Name')),
                ('template_htmldesign', models.CharField(max_length=4000, verbose_name='HTML design')),
                ('is_active', models.BooleanField()),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modified_timestamp', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='memotemplatecreated_by_user', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='memotemplatemodified_by_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
