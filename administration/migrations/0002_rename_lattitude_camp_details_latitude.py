# Generated by Django 5.0.4 on 2024-04-14 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='camp_details',
            old_name='lattitude',
            new_name='latitude',
        ),
    ]
