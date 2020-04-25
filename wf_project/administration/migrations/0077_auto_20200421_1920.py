# Generated by Django 3.0.5 on 2020-04-21 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administration', '0076_auto_20200421_1900'),
    ]

    operations = [
        migrations.CreateModel(
            name='UtiliyGroupMaintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_group_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField()),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modified_timestamp', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='utilityaccountgroupcreated_by_user', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='utilityaccountgroupmodified_by_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='utiliyaccounttypemaintenance',
            name='utility_group',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='administration.UtiliyGroupMaintenance', verbose_name='Utility Group'),
        ),
    ]
