# Generated by Django 3.2.8 on 2021-10-31 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gcampuscore", "0023_auto_20211011_2157"),
    ]

    operations = [
        migrations.AlterField(
            model_name="measurement",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="parameter",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="parametertype",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
