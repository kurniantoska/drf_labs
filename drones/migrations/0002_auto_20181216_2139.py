# Generated by Django 2.1.4 on 2018-12-16 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drones', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='drone',
            old_name='has_it_completed',
            new_name='has_it_competed',
        ),
    ]
