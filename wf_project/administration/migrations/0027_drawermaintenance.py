# Generated by Django 3.0.3 on 2020-03-20 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0026_auto_20200311_1814'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrawerMaintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drawer_name', models.CharField(max_length=250)),
                ('open_year', models.PositiveIntegerField()),
                ('open_month', models.CharField(choices=[('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], max_length=20)),
                ('limit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('drawer_status', models.CharField(choices=[('O', 'Open'), ('C', 'Closed')], max_length=10)),
                ('branch', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='administration.BranchMaintenance')),
            ],
        ),
    ]