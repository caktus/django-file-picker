# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('file_size', models.PositiveIntegerField(null=True, blank=True)),
                ('file_type', models.CharField(max_length=16, blank=True)),
                ('date_created', models.DateTimeField()),
                ('date_modified', models.DateTimeField()),
                ('file', models.FileField(upload_to=b'uploads/files/')),
                ('created_by', models.ForeignKey(related_name=b'uploads_file_created', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
                ('modified_by', models.ForeignKey(related_name=b'uploads_file_modified', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('-date_modified',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('file_size', models.PositiveIntegerField(null=True, blank=True)),
                ('file_type', models.CharField(max_length=16, blank=True)),
                ('date_created', models.DateTimeField()),
                ('date_modified', models.DateTimeField()),
                ('file', models.ImageField(upload_to=b'uploads/images/')),
                ('created_by', models.ForeignKey(related_name=b'uploads_image_created', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
                ('modified_by', models.ForeignKey(related_name=b'uploads_image_modified', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('-date_modified',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
