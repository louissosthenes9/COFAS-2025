# Generated by Django 4.2.15 on 2024-08-30 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('institution', models.CharField(max_length=200)),
                ('program', models.CharField(max_length=200)),
                ('level_of_study', models.CharField(choices=[('undergraduate', 'Undergraduate'), ('masters', 'Masters'), ('phd', 'PhD')], max_length=20)),
                ('year_of_study', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=2)),
                ('unit', models.CharField(choices=[('ict', 'ICT'), ('research', 'Research and Development')], max_length=50)),
                ('department', models.CharField(choices=[('software', 'Software Development'), ('networking', 'Computer Networking')], max_length=50)),
                ('reference_letter', models.FileField(upload_to='reference_letters/')),
                ('resume', models.FileField(upload_to='resumes/')),
                ('academic_transcript', models.FileField(upload_to='transcripts/')),
            ],
        ),
    ]