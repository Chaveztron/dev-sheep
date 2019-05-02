# Generated by Django 2.1 on 2018-08-14 03:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="ChatRoom",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="receiver",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sender",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.CharField(max_length=1200)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "conversation",
                    models.ForeignKey(
                        default=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="conversation",
                        to="chat.ChatRoom",
                    ),
                ),
                (
                    "receiver1",
                    models.ForeignKey(
                        default=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="receiver1",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender1",
                    models.ForeignKey(
                        default=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sender1",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ("timestamp",)},
        ),
    ]
