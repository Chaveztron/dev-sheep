# Generated by Django 2.1.7 on 2019-04-22 10:08

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0024_auto_20190421_0635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='telefono',
            field=phone_field.models.PhoneField(blank=True, help_text='Numero telefónico', max_length=31),
        ),
    ]