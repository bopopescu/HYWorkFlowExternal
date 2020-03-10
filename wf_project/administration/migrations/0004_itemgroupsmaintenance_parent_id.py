# Generated by Django 3.0.3 on 2020-02-25 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0003_itemclassesmaintenance_itemgroupsmaintenance_locationmaintenance'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemgroupsmaintenance',
            name='parent_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='administration.ItemGroupsMaintenance', verbose_name='Parent Group'),
        ),
    ]