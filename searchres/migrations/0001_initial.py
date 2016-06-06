# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-30 18:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(db_index=True, max_length=255)),
                ('domain', models.CharField(db_index=True, max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=20)),
                ('encoding', models.CharField(max_length=20)),
                ('contents', models.TextField()),
                ('plaintext', models.TextField()),
                ('indexed_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='DocumentMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('A', models.IntegerField(db_index=True)),
                ('B', models.IntegerField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentStemMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('type', models.IntegerField()),
                ('doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='searchres.Document')),
            ],
        ),
        migrations.CreateModel(
            name='IndexerTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('type', models.CharField(max_length=100)),
                ('parameters', models.TextField()),
                ('completed', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('depth', models.IntegerField()),
                ('parent', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Stem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stem', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='documentstemmap',
            name='stem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='searchres.Stem'),
        ),
    ]
