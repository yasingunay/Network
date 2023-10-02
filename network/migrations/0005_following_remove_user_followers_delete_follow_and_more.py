# Generated by Django 4.2.5 on 2023-10-02 11:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "network",
            "0004_follow_user_followers_delete_profile_follow_follower_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Following",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="user",
            name="followers",
        ),
        migrations.DeleteModel(
            name="Follow",
        ),
        migrations.AddField(
            model_name="following",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="following",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="following",
            name="user_followed",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="followers",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
