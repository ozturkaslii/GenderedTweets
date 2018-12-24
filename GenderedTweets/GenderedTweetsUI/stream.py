import tweepy
import config
import psycopg2
from datetime import date, timedelta
from decouple import config as db_config


class TwitterStreamer:

    @staticmethod
    def fetch_tweet():
        auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
        auth.set_access_token(config.access_token, config.access_secret)
        api = tweepy.API(auth)
        start_date = date.today() - timedelta(2)
        end_date = date.today() - timedelta(1)
        output = []

        hash_tag_list = ["woman", "man", "bitch", "skinny", "whore", "slut", "hoe", "pussy", "nipple", "ass",
                         "chick", "naked", "boobs", "motherfucker"]

        connection = psycopg2.connect(database='genderedtweetsdb',
                                      user=db_config('DB_USER'),
                                      password=db_config('DB_PASS'),
                                      host=db_config('DB_HOST'),
                                      port=db_config('DB_PORT'))
        cur = connection.cursor()

        for tag in hash_tag_list:
            for tweet in tweepy.Cursor(api.search, q=tag, count=200, since=start_date, until=end_date, lang='en').items(25):
                if not tweet.text.startswith("RT"):
                    tweet_data = []
                    tweet_data.append(tweet.id_str)
                    tweet_data.append(tweet.created_at)
                    tweet_data.append(tweet.text)
                    tweet_data.append(tweet.retweet_count)
                    tweet_data.append(tweet.favorite_count)
                    tweet_data.append(tweet.author.id_str)
                    tweet_data.append(tweet.author.name)
                    tweet_data.append(tweet.author.screen_name)
                    tweet_data.append(tweet.author.location)
                    output.append(tweet_data)

                    cur.execute("""INSERT INTO Tweet(tweet_id_str,created_at, text, retweet_count,favorite_count, 
                                            user_id_str, user_name, user_screen_name, user_location)
                                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", tweet_data)

        connection.commit()
        connection.close()

        print("finished...")

