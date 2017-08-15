# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smallurl', '0002_auto_20170810_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='hashedurl',
            name='redirect_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
