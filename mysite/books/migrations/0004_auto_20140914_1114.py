# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20140914_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publication_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
