# Generated by Django 3.0.3 on 2020-03-10 02:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0016_taxmaintenance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taxmaintenance',
            old_name='tax_cde',
            new_name='tax_code',
        ),
    ]
