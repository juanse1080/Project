# Generated by Django 3.0.2 on 2020-06-30 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0006_auto_20200630_0339'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='state',
            field=models.CharField(default='created', max_length=10),
        ),
    ]
