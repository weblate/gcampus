# Generated by Django 3.2.9 on 2021-11-22 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gcampuscore", "0024_auto_20211031_1155"),
    ]

    operations = [
        migrations.AlterField(
            model_name="measurement",
            name="water_name",
            field=models.CharField(
                help_text="Name of the water the measurement was conducted at",
                max_length=280,
                null=True,
                verbose_name="Water name",
            ),
        ),
    ]
