# Generated by Django 3.0.3 on 2020-04-13 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('approval', '0008_auto_20200409_1247'),
        ('staff_overtime', '0005_auto_20200413_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffot',
            name='approval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='approval.ApprovalItem', verbose_name='Approval'),
        ),
    ]
