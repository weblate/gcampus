# Generated by Django 3.1.7 on 2021-06-04 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcampuscore', '0017_measurement_water_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapoint',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name='Hidden'),
        ),
        migrations.AddField(
            model_name='measurement',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name='Hidden'),
        ),
    ]
