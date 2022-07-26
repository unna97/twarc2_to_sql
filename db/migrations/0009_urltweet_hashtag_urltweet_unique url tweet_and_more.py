# Generated by Django 4.0.6 on 2022-07-28 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0008_rename_in_reply_to_user_id_replied_in_reply_to_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="UrlTweet",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("start", models.IntegerField()),
                ("end", models.IntegerField()),
                ("url", models.TextField()),
                ("expanded_url", models.TextField()),
                ("display_url", models.TextField()),
                (
                    "tweet",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tweet_url",
                        to="db.tweet",
                    ),
                ),
            ],
            options={
                "db_table": "url_tweet_mapping",
            },
        ),
        migrations.CreateModel(
            name="HashTag",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("start", models.IntegerField()),
                ("end", models.IntegerField()),
                ("tag", models.TextField()),
                (
                    "tweet",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tweet_hashtag",
                        to="db.tweet",
                    ),
                ),
            ],
            options={
                "db_table": "hashtag_tweet_mapping",
            },
        ),
        migrations.AddConstraint(
            model_name="urltweet",
            constraint=models.UniqueConstraint(
                fields=("tweet", "start"), name="unique url tweet"
            ),
        ),
        migrations.AddConstraint(
            model_name="hashtag",
            constraint=models.UniqueConstraint(
                fields=("tweet", "start"), name="unique hashtag tweet"
            ),
        ),
    ]
