# Generated by Django 3.0.2 on 2020-06-11 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='docker',
            old_name='proto_path',
            new_name='proto',
        ),
    ]
