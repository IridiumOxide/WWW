# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gmina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numer', models.IntegerField()),
                ('nazwa', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Obwod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numer', models.IntegerField()),
                ('adres', models.CharField(max_length=128)),
                ('otrzymanych_kart', models.IntegerField(default=0)),
                ('uprawnionych', models.IntegerField(default=0)),
                ('gmina', models.ForeignKey(to='apka.Gmina')),
            ],
        ),
    ]
