# Generated by Django 2.2.5 on 2019-12-04 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docker', '0002_auto_20191204_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docker',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]