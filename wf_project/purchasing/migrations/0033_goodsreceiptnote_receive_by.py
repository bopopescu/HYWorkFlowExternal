# Generated by Django 3.0.5 on 2020-04-20 17:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('purchasing', '0032_auto_20200420_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodsreceiptnote',
            name='receive_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
