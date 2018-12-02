# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enfermedad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('images', models.IntegerField()),
                ('planta', models.CharField(max_length=50)),
                ('sintomaAA', models.CharField(max_length=50)),
                ('sintomaBB', models.CharField(max_length=50)),
                ('sintomaCC', models.CharField(max_length=50)),
                ('sintomaDD', models.CharField(max_length=50)),
                ('sintomaEE', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Enfermedadmaes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('images', models.IntegerField()),
                ('planta', models.CharField(max_length=50)),
                ('sintomaAA', models.CharField(max_length=50)),
                ('sintomaBB', models.CharField(max_length=50)),
                ('sintomaCC', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Enfermedadmara',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('images', models.IntegerField()),
                ('planta', models.CharField(max_length=50)),
                ('sintomaAA', models.CharField(max_length=50)),
                ('sintomaBB', models.CharField(max_length=50)),
                ('sintomaCC', models.CharField(max_length=50)),
                ('sintomaDD', models.CharField(max_length=50)),
                ('sintomaEE', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Enfermedadsoho',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('images', models.IntegerField()),
                ('planta', models.CharField(max_length=50)),
                ('sintomaAA', models.CharField(max_length=50)),
                ('sintomaBB', models.CharField(max_length=50)),
                ('sintomaCC', models.CharField(max_length=50)),
                ('sintomaDD', models.CharField(max_length=50)),
                ('sintomaEE', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Enfermedadsora',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('images', models.IntegerField()),
                ('planta', models.CharField(max_length=50)),
                ('sintomaAA', models.CharField(max_length=50)),
                ('sintomaBB', models.CharField(max_length=50)),
                ('sintomaCC', models.CharField(max_length=50)),
                ('sintomaDD', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Enfermedadsota',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('images', models.IntegerField()),
                ('planta', models.CharField(max_length=50)),
                ('sintomaAA', models.CharField(max_length=50)),
                ('sintomaBB', models.CharField(max_length=50)),
                ('sintomaCC', models.CharField(max_length=50)),
                ('sintomaDD', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Enfermedadtriho',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('images', models.IntegerField()),
                ('planta', models.CharField(max_length=50)),
                ('sintomaAA', models.CharField(max_length=50)),
                ('sintomaBB', models.CharField(max_length=50)),
                ('sintomaCC', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Enfermedadtripla',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('images', models.IntegerField()),
                ('planta', models.CharField(max_length=50)),
                ('sintomaAA', models.CharField(max_length=50)),
                ('sintomaBB', models.CharField(max_length=50)),
                ('sintomaCC', models.CharField(max_length=50)),
                ('sintomaDD', models.CharField(max_length=50)),
                ('sintomaEE', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Mireview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('reviewer', models.CharField(max_length=50)),
                ('createdTime', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enfermedadName', models.CharField(max_length=50)),
                ('enfermedadId', models.IntegerField()),
                ('comment', models.TextField()),
                ('reviewer', models.CharField(max_length=50)),
                ('stars', models.IntegerField()),
                ('createdTime', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reviewmaes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enfermedadName', models.CharField(max_length=50)),
                ('enfermedadId', models.IntegerField()),
                ('comment', models.TextField()),
                ('reviewer', models.CharField(max_length=50)),
                ('stars', models.IntegerField()),
                ('createdTime', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reviewmara',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enfermedadName', models.CharField(max_length=50)),
                ('enfermedadId', models.IntegerField()),
                ('comment', models.TextField()),
                ('reviewer', models.CharField(max_length=50)),
                ('stars', models.IntegerField()),
                ('createdTime', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reviewsoho',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enfermedadName', models.CharField(max_length=50)),
                ('enfermedadId', models.IntegerField()),
                ('comment', models.TextField()),
                ('reviewer', models.CharField(max_length=50)),
                ('stars', models.IntegerField()),
                ('createdTime', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reviewsora',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enfermedadName', models.CharField(max_length=50)),
                ('enfermedadId', models.IntegerField()),
                ('comment', models.TextField()),
                ('reviewer', models.CharField(max_length=50)),
                ('stars', models.IntegerField()),
                ('createdTime', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reviewsota',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enfermedadName', models.CharField(max_length=50)),
                ('enfermedadId', models.IntegerField()),
                ('comment', models.TextField()),
                ('reviewer', models.CharField(max_length=50)),
                ('stars', models.IntegerField()),
                ('createdTime', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reviewtriho',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enfermedadName', models.CharField(max_length=50)),
                ('enfermedadId', models.IntegerField()),
                ('comment', models.TextField()),
                ('reviewer', models.CharField(max_length=50)),
                ('stars', models.IntegerField()),
                ('createdTime', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reviewtripla',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enfermedadName', models.CharField(max_length=50)),
                ('enfermedadId', models.IntegerField()),
                ('comment', models.TextField()),
                ('reviewer', models.CharField(max_length=50)),
                ('stars', models.IntegerField()),
                ('createdTime', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enfermedadName', models.CharField(max_length=50)),
                ('enfermedadId', models.IntegerField()),
                ('attribute', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
            ],
        ),
    ]
