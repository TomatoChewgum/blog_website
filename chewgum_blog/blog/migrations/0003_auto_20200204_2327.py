# Generated by Django 3.0.3 on 2020-02-04 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200203_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='pv',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='uv',
            field=models.PositiveIntegerField(default=0),
        ),
    ]