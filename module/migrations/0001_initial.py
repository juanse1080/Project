# Generated by Django 3.0.2 on 2020-06-16 03:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Docker',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('ip', models.CharField(max_length=30, null=True, unique=True)),
                ('language', models.CharField(choices=[('python', 'Python')], default='python', max_length=100)),
                ('proto', models.CharField(max_length=500, null=True)),
                ('path', models.CharField(max_length=500, null=True)),
                ('image', models.CharField(max_length=500, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_file', models.CharField(max_length=500, null=True)),
                ('output_file', models.CharField(max_length=500, null=True)),
                ('response', models.CharField(max_length=1000, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('docker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='experiments', to='module.Docker')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='experiments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='graphs', to='module.Experiment')),
            ],
        ),
        migrations.CreateModel(
            name='GraphType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('bar', 'Bar graphic'), ('donut', 'Donut chart')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('graph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='series', to='module.Graph')),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.CharField(blank=True, max_length=100, null=True)),
                ('y', models.FloatField(blank=True, max_length=100, null=True)),
                ('serie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points', to='module.Serie')),
            ],
        ),
        migrations.CreateModel(
            name='ElementType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=30)),
                ('len', models.CharField(default=0, max_length=1)),
                ('value', models.TextField()),
                ('docker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elements_type', to='module.Docker')),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types', to='module.Element')),
            ],
        ),
    ]
