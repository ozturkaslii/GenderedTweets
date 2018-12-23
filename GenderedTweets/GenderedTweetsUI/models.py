from django.db import models
from django.contrib.postgres.fields import JSONField


class Tweet(models.Model):
    id = models.BigAutoField(primary_key=True)
    tweet_id_str = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateField(null=True, blank=True)
    text = models.CharField(max_length=300, null=True, blank=True)
    user_id_str = models.CharField(max_length=250, null=True, blank=True)
    user_name = models.CharField(max_length=150, null=True, blank=True)
    user_screen_name = models.CharField(max_length=150, null=True, blank=True)
    user_location = models.CharField(max_length=150, null=True, blank=True)
    quote_count = models.IntegerField(null=True, blank=True)
    reply_count = models.IntegerField(null=True, blank=True)
    retweet_count = models.IntegerField(null=True, blank=True)
    favorite_count = models.IntegerField(null=True, blank=True)


