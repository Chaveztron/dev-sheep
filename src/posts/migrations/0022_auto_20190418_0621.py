# Generated by Django 2.1.7 on 2019-04-18 06:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0021_auto_20190418_0619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='cv',
            field=models.FileField(default='default.pdf', upload_to='cvs', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]
