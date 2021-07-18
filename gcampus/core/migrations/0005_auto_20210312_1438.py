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

# Generated by Django 3.1.7 on 2021-03-12 13:38

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gcampuscore", "0004_auto_20210310_1205"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="datapoint",
            options={
                "verbose_name": "Data point",
                "verbose_name_plural": "Data points",
            },
        ),
        migrations.AlterModelOptions(
            name="datatype",
            options={"verbose_name": "Data type", "verbose_name_plural": "Data types"},
        ),
        migrations.AlterModelOptions(
            name="measurement",
            options={
                "verbose_name": "Measurement",
                "verbose_name_plural": "Measurements",
            },
        ),
        migrations.AlterField(
            model_name="datapoint",
            name="comment",
            field=models.TextField(blank=True, verbose_name="Comment"),
        ),
        migrations.AlterField(
            model_name="datapoint",
            name="data_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="gcampuscore.datatype",
                verbose_name="Data type",
            ),
        ),
        migrations.AlterField(
            model_name="datapoint",
            name="measurement",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="gcampuscore.measurement",
                verbose_name="Associated measurement",
            ),
        ),
        migrations.AlterField(
            model_name="datapoint",
            name="value",
            field=models.FloatField(verbose_name="Value"),
        ),
        migrations.AlterField(
            model_name="datatype",
            name="name",
            field=models.CharField(blank=True, max_length=280, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="measurement",
            name="comment",
            field=models.TextField(blank=True, verbose_name="Comment"),
        ),
        migrations.AlterField(
            model_name="measurement",
            name="location",
            field=django.contrib.gis.db.models.fields.PointField(
                srid=4326, verbose_name="Location"
            ),
        ),
        migrations.AlterField(
            model_name="measurement",
            name="location_name",
            field=models.CharField(
                blank=True,
                help_text="An approximated location for the measurement",
                max_length=280,
                null=True,
                verbose_name="Location name",
            ),
        ),
        migrations.AlterField(
            model_name="measurement",
            name="name",
            field=models.CharField(
                blank=True,
                help_text="Your name or team name",
                max_length=280,
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="measurement",
            name="time",
            field=models.DateTimeField(
                help_text="Date and time of the measurement", verbose_name="Time"
            ),
        ),
    ]
