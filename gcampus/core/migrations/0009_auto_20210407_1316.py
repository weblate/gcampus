# Generated by Django 3.1.7 on 2021-04-07 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gcampuscore", "0008_auto_20210407_1309"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datatype",
            name="unit",
            field=models.CharField(blank=True, max_length=11, verbose_name="Unit"),
        ),
    ]
