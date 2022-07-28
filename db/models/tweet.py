from django.db import models
from django.db.models import *

class Tweet(models.Model):
    class Meta:
        db_table = "tweet_data"

    id = CharField(max_length=256, primary_key=True)
    created_at = DateTimeField()
    text = TextField()
    # Figure out type of relationship
    author = ForeignKey('Author', null=True, default=True, db_constraint=False,
                        on_delete=DO_NOTHING)  # one author to many tweets
    possibly_sensitive = BooleanField()
    conversation_id = TextField()
    source = TextField()
    reply_settings = TextField(null=True)
    lang = TextField(null=True)
    retweet_count = IntegerField()
    like_count = IntegerField()
    quote_count = IntegerField()
    reply_count = IntegerField()
    # 0: tweet, 1: quoted tweet, 2: retweeted tweet, 3: replied to tweet, 4: quoted tweet + replied to tweet
    tweet_type = IntegerField()

class Author(models.Model):
    class Meta:
        db_table = "author_data"
    
    id = CharField(primary_key=True, max_length=256)


class Quote(models.Model):
    class Meta:
        db_table = "quoted_tweet_mapping"
        constraints = [
                        models.UniqueConstraint(fields=["tweet"], name='unique quote tweet')
                    ]
    
    id = AutoField(primary_key=True)
    tweet = ForeignKey("Tweet", on_delete=CASCADE, related_name="quoted_tweet")
    referenced_tweet = ForeignKey("Tweet", on_delete=DO_NOTHING, related_name="quoted_referenced_tweet", db_constraint=False)


class Retweet(models.Model):
    class Meta:
        db_table = "retweeted_tweet_mapping"
        constraints = [
            models.UniqueConstraint(fields=["tweet"], name='unique retweet tweet')
        ]

    id = AutoField(primary_key=True)
    tweet = ForeignKey("Tweet", on_delete=CASCADE, related_name="retweeted_tweet")
    referenced_tweet = ForeignKey(
        "Tweet", on_delete=DO_NOTHING, related_name="retweeted_referenced_tweet", db_constraint=False)


class Replied(models.Model):
    class Meta:
        db_table = "replied_to_tweet_mapping"
        constraints = [
            models.UniqueConstraint(fields=["tweet"], name='unique replied tweet')
        ]

    id = AutoField(primary_key=True)
    tweet = ForeignKey("Tweet", on_delete=CASCADE, related_name="replied_to_tweet")
    referenced_tweet = ForeignKey(
        "Tweet", on_delete=DO_NOTHING, related_name="replied_to_referenced_tweet", db_constraint=False)
    in_reply_to_user = ForeignKey("Author", on_delete=DO_NOTHING, related_name="in_reply_to_user_id", db_constraint=False)


class UrlTweet(models.Model):
    class Meta:
        db_table = "url_tweet_mapping"
        constraints = [
            models.UniqueConstraint(fields=["tweet","start"], name='unique url tweet')
        ]

    id = AutoField(primary_key=True)
    tweet = ForeignKey("Tweet", on_delete=CASCADE, related_name="tweet_url", db_constraint=False)
    start = IntegerField()
    end = IntegerField()
    url = TextField()
    expanded_url = TextField()
    display_url = TextField()
    

class HashTag(models.Model):
    class Meta:
        db_table = "hashtag_tweet_mapping"
        constraints = [
            models.UniqueConstraint(fields=["tweet","start"], name='unique hashtag tweet')
        ]

    id = AutoField(primary_key=True)
    tweet = ForeignKey("Tweet", on_delete=CASCADE, related_name="tweet_hashtag", db_constraint=False)
    start = IntegerField()
    end = IntegerField()
    tag = TextField()
    