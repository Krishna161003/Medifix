# Generated by Django 5.0.4 on 2024-04-23 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0003_camp_details_registration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camp_details',
            name='end_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='camp_details',
            name='start_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
