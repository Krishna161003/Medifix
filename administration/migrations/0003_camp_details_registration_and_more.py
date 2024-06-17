# Generated by Django 5.0.4 on 2024-04-21 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0002_rename_lattitude_camp_details_latitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='camp_details',
            name='registration',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='camp_details',
            name='end_date_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='camp_details',
            name='start_date_time',
            field=models.DateTimeField(blank=True),
        ),
    ]