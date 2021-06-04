# Generated by Django 3.1.7 on 2021-06-04 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcampuscore', '0016_merge_20210531_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='water_name',
            field=models.CharField(blank=True, help_text='Name of the water the measurement was conducted at', max_length=280, null=True, verbose_name='Water name'),
        ),
    ]