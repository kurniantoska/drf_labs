# Generated by Django 2.1.4 on 2018-12-17 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drones', '0002_auto_20181216_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='drone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competitions', to='drones.Drone'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='pilot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competitions', to='drones.Pilot'),
        ),
    ]
