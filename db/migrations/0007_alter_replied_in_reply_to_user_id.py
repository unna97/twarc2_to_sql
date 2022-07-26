# Generated by Django 4.0.6 on 2022-07-26 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_alter_quote_referenced_tweet_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='replied',
            name='in_reply_to_user_id',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='in_reply_to_user_id', to='db.author'),
        ),
    ]
