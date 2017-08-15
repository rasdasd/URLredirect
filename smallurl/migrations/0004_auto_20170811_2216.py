# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('smallurl', '0003_hashedurl_redirect_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('referer', models.CharField(max_length=1000)),
                ('user_agent', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip', models.GenericIPAddressField()),
            ],
        ),
        migrations.RenameField(
            model_name='hashedurl',
            old_name='created_date',
            new_name='timestamp',
        ),
        migrations.AddField(
            model_name='hashedurl',
            name='ip',
            field=models.GenericIPAddressField(default='000.000.000.000'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='redirect',
            name='hashedUrl',
            field=models.ForeignKey(to='smallurl.HashedURL'),
        ),
    ]
