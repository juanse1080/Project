# Generated by Django 2.2.5 on 2019-12-18 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graph',
            name='y',
            field=models.FloatField(max_length=100),
        ),
    ]