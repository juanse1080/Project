# Generated by Django 2.2.5 on 2020-02-12 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0004_auto_20200212_1218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='point',
            name='kind',
        ),
    ]