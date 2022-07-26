# Generated by Django 4.0.6 on 2022-07-29 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0012_mentions_cashtag_mentions_unique mentions tweet_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="replied",
            name="tweet",
            field=models.ForeignKey(
                db_constraint=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="replied_to_tweet",
                to="db.tweet",
            ),
        ),
    ]
