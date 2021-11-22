# Generated by Django 3.1.7 on 2021-10-11 19:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gcampuscore", "0022_auto_20211011_2111"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="DataType",
            new_name="ParameterType",
        ),
        migrations.AlterModelOptions(
            name="parameter",
            options={
                "default_manager_name": "all_objects",
                "verbose_name": "Parameter",
                "verbose_name_plural": "Parameters",
            },
        ),
        migrations.AlterModelOptions(
            name="parametertype",
            options={
                "verbose_name": "Parameter type",
                "verbose_name_plural": "Parameter types",
            },
        ),
        migrations.RenameField(
            model_name="parameter", old_name="data_type", new_name="parameter_type"
        ),
        migrations.AlterField(
            model_name="parameter",
            name="parameter_type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="parameters",
                to="gcampuscore.parametertype",
                verbose_name="Parameter type",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="parameter",
            name="measurement",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="parameters",
                to="gcampuscore.measurement",
                verbose_name="Associated measurement",
            ),
        ),
    ]
