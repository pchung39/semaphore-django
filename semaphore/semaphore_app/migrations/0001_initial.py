# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 06:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance', models.CharField(max_length=100)),
                ('instance_provider', models.CharField(max_length=100)),
                ('provider_service', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PingResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance', models.CharField(max_length=100)),
                ('min_ping', models.DecimalField(decimal_places=4, max_digits=10)),
                ('max_ping', models.DecimalField(decimal_places=4, max_digits=10)),
                ('avg_ping', models.DecimalField(decimal_places=4, max_digits=10)),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=25)),
                ('password', models.CharField(max_length=25)),
                ('email', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='pingresults',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='semaphore_app.Users'),
        ),
        migrations.AddField(
            model_name='instance',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='semaphore_app.Users'),
        ),
    ]