#  Copyright (C) 2021 desklab gUG
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Generated by Django 3.1.7 on 2021-03-08 15:59

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DataType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=280)),
            ],
        ),
        migrations.CreateModel(
            name="Measurement",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=280)),
                ("location", django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ("time", models.DateTimeField()),
                ("comment", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="DataPoint",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.FloatField()),
                ("comment", models.TextField(blank=True)),
                (
                    "data_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="gcampuscore.datatype",
                    ),
                ),
                (
                    "measurement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="gcampuscore.measurement",
                    ),
                ),
            ],
        ),
    ]
