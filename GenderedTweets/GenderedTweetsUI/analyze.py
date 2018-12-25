import re
import pandas as pd
import psycopg2
from decouple import config as db_config
from textblob import TextBlob


class Text:
    @staticmethod
    def word_in_text(word, text):
        word = word.lower()
        text = text.lower()
        match = re.search(word, text)
        if match:
            return True
        else:
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


class TweetsToDataSet:

    @property
    def tweets_to_data_set(self):
        results = GetTweets().get_tweets
        id_list = [tweet[0] for tweet in results]
        data_set = pd.DataFrame(id_list, columns=["id"])
        data_set["text"] = [tweet[3] for tweet in results]

        return data_set


class AnalyzeTweets:

    def process_results(self):
        data_set = TweetsToDataSet().tweets_to_data_set

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


class SentimentAnalysis:

    def clean_tweet(self, tweets):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweets).split())

    def analyze_sentiment(self, tweets):
        analysis = TextBlob(self.clean_tweet(tweets))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity < 0:
            return -1
        else:
            return 0

    def woman_sentiment(self, tweets):
        data_set = TweetsToDataSet().tweets_to_data_set
        data_set['woman'] = data_set['text'].apply(lambda tweet: Text.word_in_text('woman', tweet))
        data_set['sentiment'] = [self.analyze_sentiment(tweet[3]) for tweet in tweets]

        count_pos = 0

        for key, val in data_set['woman'].items():
            if val:
                if data_set['sentiment'][key] == 1:
                    count_pos += 1

        return count_pos

    def man_sentiment(self, tweets):
        data_set = TweetsToDataSet().tweets_to_data_set
        data_set['man'] = data_set['text'].apply(lambda tweet: Text.word_in_text('man', tweet))
        data_set['sentiment'] = [self.analyze_sentiment(tweet[3]) for tweet in tweets]

        count_pos = 0

        for key, val in data_set['man'].items():
            if val:
                if data_set['sentiment'][key] == 1:
                    count_pos += 1

        return count_pos

    @property
    def total_woman_man(self):
        data_set = TweetsToDataSet().tweets_to_data_set
        data_set['woman'] = data_set['text'].apply(lambda tweet: Text.word_in_text('woman', tweet))
        data_set['man'] = data_set['text'].apply(lambda tweet: Text.word_in_text('man', tweet))
        man = int(data_set['man'].value_counts()[True])
        woman = int(data_set['woman'].value_counts()[True])
        total = woman + man

        return total

    def calculate_woman(self, tweets):
        total = self.total_woman_man
        woman_positive = self.woman_sentiment(tweets)
        calc = (woman_positive/total)*100

        return calc

    def calculate_man(self, tweets):
        total = self.total_woman_man
        man_positive = self.man_sentiment(tweets)
        calc = (man_positive / total) * 100

        return calc

    def update_data_set(self, tweets):
        data_set = TweetsToDataSet().tweets_to_data_set
        import pdb
        # pdb.set_trace()
        data_set['sentiment'] = [self.analyze_sentiment(tweet[3]) for tweet in tweets]

        return data_set
