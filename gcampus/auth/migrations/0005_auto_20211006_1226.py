# Generated by Django 3.1.7 on 2021-10-06 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("gcampusauth", "0004_coursetoken_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="coursetoken",
            old_name="name",
            new_name="token_name",
        ),
    ]