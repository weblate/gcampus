# Generated by Django 3.2.9 on 2021-11-22 10:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gcampusauth", "0008_alter_coursetoken_teacher_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accesskey",
            name="parent_token",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="access_keys",
                to="gcampusauth.coursetoken",
            ),
        ),
    ]
