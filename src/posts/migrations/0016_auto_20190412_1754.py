# Generated by Django 2.1.7 on 2019-04-12 17:54

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_postview_telefono'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postview',
            name='telefono',
        ),
        migrations.AddField(
            model_name='author',
            name='telefono',
            field=phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31),
        ),
    ]
