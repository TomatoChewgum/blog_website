# Generated by Django 3.0.3 on 2020-02-14 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Valentinephoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='图片名称')),
                ('photo', models.ImageField(upload_to='valentinephoto/%Y%m%d/')),
                ('words', models.CharField(max_length=255, verbose_name='介绍')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]