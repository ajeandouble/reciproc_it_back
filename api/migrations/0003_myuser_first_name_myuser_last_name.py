# Generated by Django 4.0.4 on 2022-05-20 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_myuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='first_name',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myuser',
            name='last_name',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]