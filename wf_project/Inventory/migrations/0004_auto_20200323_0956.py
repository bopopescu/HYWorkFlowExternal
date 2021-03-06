# Generated by Django 3.0.3 on 2020-03-23 01:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0034_auto_20200322_1840'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Inventory', '0003_auto_20200320_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='itemcreated_by_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='created_timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='item_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.ItemClassesMaintenance', verbose_name='Item Class'),
        ),
        migrations.AlterField(
            model_name='item',
            name='item_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.ItemGroupsMaintenance', verbose_name='Item Group'),
        ),
        migrations.AlterField(
            model_name='item',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='itemmodified_by_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='modified_timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
