# Generated by Django 3.0.5 on 2020-04-24 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0078_hrplatformmaintenance'),
        ('human_resource', '0018_auto_20200404_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffPlatform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('success_platform', models.BooleanField(max_length=250, verbose_name='Is Success Platform?')),
                ('platform_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.HRPlatformMaintenance')),
                ('staff_recruitment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='human_resource.StaffRecruitmentRequest')),
            ],
        ),
        migrations.CreateModel(
            name='StaffCandidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate_name', models.CharField(max_length=250, verbose_name='Candidate Name')),
                ('date_of_join', models.CharField(max_length=250, verbose_name='Date Of Join')),
                ('staff_recruitment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='human_resource.StaffRecruitmentRequest')),
            ],
        ),
    ]