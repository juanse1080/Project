# Generated by Django 3.0.2 on 2020-06-28 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0003_auto_20200628_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='docker',
            name='build',
        ),
    ]
