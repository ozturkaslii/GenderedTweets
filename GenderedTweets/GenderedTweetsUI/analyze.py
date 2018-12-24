import re

import pandas as pd
import psycopg2
from decouple import config as db_config


class Text:
    @staticmethod
    def word_in_text(word, text):
        word = word.lower()
        text = text.lower()
        match = re.search(word, text)
        if match:
            return True
        return False


class GetTweets:

    @property
    def get_tweets(self):
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


class AnalyzeTweets:

    def process_results(self):
        results = GetTweets().get_tweets
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

    def count_keywords(self):
        data_set = self.process_results()

        tweets_by_sexist_keywords = {
            'bitch': int(data_set['bitch'].value_counts()[True]),
            'skinny': int(data_set['skinny'].value_counts()[True]),
            'whore': int(data_set['whore'].value_counts()[True]),
            'slut': int(data_set['slut'].value_counts()[True]),
            'hoe': int(data_set['hoe'].value_counts()[True]),
            'pussy': int(data_set['pussy'].value_counts()[True]),
            'nipple': int(data_set['nipple'].value_counts()[True]),
            'ass': int(data_set['ass'].value_counts()[True]),
            'boobs': int(data_set['boobs'].value_counts()[True]),
            'motherfucker': int(data_set['motherfucker'].value_counts()[True])
        }

        return tweets_by_sexist_keywords

    def tweet_count(self):
        tweets_by_sexist_keywords = self.count_keywords()
        dict_val = tweets_by_sexist_keywords.values()
        sorted_tweets = sorted(dict_val, reverse=True)
        return sorted_tweets[:5]

    def tweet_label(self):
        tweets_by_sexist_keywords = self.count_keywords()
        label_list = []

        for i in AnalyzeTweets.tweet_count(self):
            for key, val in tweets_by_sexist_keywords.items():
                if i == val:
                    label_list.append(key)

        return label_list
