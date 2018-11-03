# -*- coding: utf-8 -*-
"""
Stream all tweets based on specific keywords

@author: Aslı Öztürk
"""

from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import config


class TwitterAuthenticator():
    
    def authenticate_twitter_app(self):
        auth = OAuthHandler(config.consumer_key, config.consumer_secret)
        auth.set_access_token(config.access_token, config.access_secret)
        return auth
    
    
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authentication and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)


class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          

    def on_error(self, status):
        if status == 420:
            # Returning false on_data method in case rate limit occurs
            return False
        print(status)
        
if __name__ == '__main__':    

    # Authenticate using config.py and connect to Twitter Streaming API.
    hash_tag_list = ["woman", "man", "bitch", "skinny", "whore", "slut", "hoe", "pussy", "nipple", "ass", "chick", 
                     "naked", "boobs", "motherfucker", "as a woman", "as a man", "skinny girl", "pussy cat",
                     "woman should do", "woman should wear", "i'm not trying to be sexist but", 
                     "i'm not trying to be sexist or", "i'm not sexist but", "nagging wife"]
    fetched_tweets_filename = "allTweets.json"
    

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)        
        
        
        
        
        
        
        
        
        
        
        