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

# Generated by Django 3.1.7 on 2021-05-30 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gcampuscore", "0014_measurement_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studenttoken",
            name="token",
            field=models.CharField(max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name="teachertoken",
            name="token",
            field=models.CharField(max_length=12, unique=True),
        ),
    ]
