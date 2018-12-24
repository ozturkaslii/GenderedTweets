import tweepy
import config
import psycopg2
from datetime import date, timedelta
from decouple import config as db_config
import re
import pandas as pd
import numpy as np


class Text:
    @staticmethod
    def word_in_text(word, text):
        word = word.lower()
        text = text.lower()
        match = re.search(word, text)
        if match:
            return True
        return False


class AnalyzeTweets:

    @staticmethod
    def get_tweets():
        connection = psycopg2.connect(database='genderedtweetsdb',
                                      user=db_config('DB_USER'),
                                      password=db_config('DB_PASS'),
                                      host=db_config('DB_HOST'),
                                      port=db_config('DB_PORT'))
        cur = connection.cursor()

        cur.execute("SELECT * FROM tweet")
        results = cur.fetchall()
        connection.commit()
        connection.close()

        return results

    def process_results(self, results):
        id_list = [tweet[0] for tweet in results]
        data_set = pd.DataFrame(id_list, columns=["id"])
        data_set["text"] = [tweet[3] for tweet in results]

        # print(data_set)

        data_set['woman'] = data_set['text'].apply(lambda tweet: Text.word_in_text('woman', tweet))
        data_set['man'] = data_set['text'].apply(lambda tweet: Text.word_in_text('man', tweet))
        data_set['bitch'] = data_set['text'].apply(lambda tweet: Text.word_in_text('bitch', tweet))
        data_set['skinny'] = data_set['text'].apply(lambda tweet: Text.word_in_text('skinny', tweet))
        data_set['whore'] = data_set['text'].apply(lambda tweet: Text.word_in_text('whore', tweet))
        data_set['slut'] = data_set['text'].apply(lambda tweet: Text.word_in_text('slut', tweet))
        data_set['hoe'] = data_set['text'].apply(lambda tweet: Text.word_in_text('hoe', tweet))
        data_set['pussy'] = data_set['text'].apply(lambda tweet: Text.word_in_text('pussy', tweet))
        data_set['nipple'] = data_set['text'].apply(lambda tweet: Text.word_in_text('nipple', tweet))
        data_set['ass'] = data_set['text'].apply(lambda tweet: Text.word_in_text('ass', tweet))
        data_set['boobs'] = data_set['text'].apply(lambda tweet: Text.word_in_text('boobs', tweet))
        data_set['motherfucker'] = data_set['text'].apply(lambda tweet: Text.word_in_text('motherfucker', tweet))

        return data_set

    def count_keywords(self, result):
        data_set = self.process_results(result)

        tweets_by_sexist_keywords = {
            'bitch': data_set['bitch'].value_counts()[True],
            'skinny': data_set['skinny'].value_counts()[True],
            'whore': data_set['whore'].value_counts()[True],
            'slut': data_set['slut'].value_counts()[True],
            'hoe': data_set['hoe'].value_counts()[True],
            'pussy': data_set['pussy'].value_counts()[True],
            'nipple': data_set['nipple'].value_counts()[True],
            'ass': data_set['ass'].value_counts()[True],
            'boobs': data_set['boobs'].value_counts()[True],
            'motherfucker': data_set['motherfucker'].value_counts()[True]
        }

        return tweets_by_sexist_keywords

    def graph_list(self, result):
        print("sssss")
        tweets_by_sexist_keywords = self.count_keywords(result)
        print(tweets_by_sexist_keywords)
        dict_val = tweets_by_sexist_keywords.values()
        sorted_tweets = sorted(dict_val, reverse=True)
        print(sorted_tweets[:5])
        return sorted_tweets[:5]

    def label_list(self, result):
        tweets_by_sexist_keywords = self.count_keywords(result)
        label_list = []

        for i in AnalyzeTweets.graph_list():
            for key, val in tweets_by_sexist_keywords.items():
                if i == val:
                    label_list.append(key)

        return label_list




