# Generated by Django 3.1.7 on 2021-03-10 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcampuscore', '0003_measurement_location_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='location_name',
            field=models.CharField(blank=True, max_length=280, null=True),
        ),
    ]
