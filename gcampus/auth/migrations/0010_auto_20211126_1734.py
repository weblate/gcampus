# Generated by Django 3.2.8 on 2021-11-26 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gcampusauth', '0009_alter_accesskey_parent_token'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accesskey',
            options={'ordering': ('created_at',), 'verbose_name': 'Access Key'},
        ),
        migrations.AlterField(
            model_name='coursetoken',
            name='token_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='Course Name'),
        ),
    ]
