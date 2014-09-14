# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20140914_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='email',
            field=models.EmailField(max_length=75, verbose_name=b'\xe7\x94\xb5\xe5\xad\x90\xe9\x82\xae\xe4\xbb\xb6', blank=True),
        ),
    ]
