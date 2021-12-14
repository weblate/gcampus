# Generated by Django 3.2.8 on 2021-12-14 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gcampuscore', '0027_auto_20211214_1202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parametertype',
            name='limit',
        ),
        migrations.AddField(
            model_name='limit',
            name='parameter_limit',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.PROTECT, related_name='parameter_limit', to='gcampuscore.parametertype', verbose_name='Parameter type'),
        ),
    ]