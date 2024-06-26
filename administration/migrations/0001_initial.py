# Generated by Django 5.0.4 on 2024-04-14 03:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='camp_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camp_name', models.CharField(max_length=200, null=True)),
                ('location', models.CharField(max_length=200, null=True)),
                ('lattitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('start_date_time', models.DateTimeField()),
                ('end_date_time', models.DateTimeField()),
                ('contact_website', models.URLField(blank=True, null=True)),
                ('hospital_name', models.CharField(blank=True, max_length=150, null=True)),
                ('club_name', models.CharField(blank=True, max_length=150, null=True)),
                ('other', models.CharField(blank=True, max_length=150, null=True)),
                ('description', models.TextField(max_length=3000, null=True)),
                ('type_of_camp', models.CharField(choices=[('Paid', 'Paid'), ('Free', 'Free')], max_length=30, null=True)),
                ('cost', models.IntegerField(blank=True, default='0', null=True)),
                ('total_camp_registrations', models.IntegerField()),
                ('camp_register_active', models.BooleanField(default=False)),
                ('createdby', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='camp_services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=200, null=True)),
                ('camp_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.camp_details')),
            ],
        ),
        migrations.CreateModel(
            name='doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_name', models.CharField(max_length=255, null=True)),
                ('doctor_title', models.CharField(max_length=255, null=True)),
                ('doctor_description', models.CharField(max_length=255, null=True)),
                ('camp_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administration.camp_details')),
            ],
        ),
        migrations.CreateModel(
            name='profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.IntegerField(blank=True, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('camp_register', models.BooleanField(default=False)),
                ('submitted_application', models.BooleanField(default=False)),
                ('about', models.TextField(blank=True, max_length=2000, null=True)),
                ('user_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
