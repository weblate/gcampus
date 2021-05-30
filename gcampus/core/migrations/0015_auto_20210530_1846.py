# Generated by Django 3.1.7 on 2021-05-30 16:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("gcampuscore", "0014_measurement_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="studenttoken",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="studenttoken",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="teachertoken",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="teachertoken",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="datatype",
            name="unit",
            field=models.CharField(blank=True, max_length=10, verbose_name="Unit"),
        ),
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
