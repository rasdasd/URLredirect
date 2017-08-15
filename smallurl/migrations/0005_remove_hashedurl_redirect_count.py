# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smallurl', '0004_auto_20170811_2216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hashedurl',
            name='redirect_count',
        ),
    ]
