from django.views import generic
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Tweet
from django.http import JsonResponse
from django.shortcuts import render
from GenderedTweetsUI.stream import TwitterStreamer
from GenderedTweetsUI.analyze import AnalyzeTweets, Text
import psycopg2
from decouple import config as db_config
import pandas as pdd
import re


class IndexView(generic.ListView):
    # stream = TwitterStreamer.fetch_tweet()

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

    id_list = [tweet[0] for tweet in results]
    data_set = pdd.DataFrame(id_list, columns=["id"])
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

    print('woman', data_set['woman'].value_counts()[True])

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

    dict_key = tweets_by_sexist_keywords.keys()
    dict_val = tweets_by_sexist_keywords.values()
    sorted_tweets = sorted(dict_val, reverse=True)

    graph_list = sorted_tweets[:5]

    # print(tweets_by_sexist_keywords)

    label_list = []

    for i in graph_list:
        for key, val in tweets_by_sexist_keywords.items():
            if i == val:
                label_list.append(key)

    # print(graph_list)
    # print(label_list)



    def get(self, request):
        return render(request, 'GenderedTweetsUI/index.html')

    def get_data(request, *args, **kwargs):
        # we will use dictionary here
        labels = IndexView.label_list
        default_items = IndexView.graph_list
        data = dict(labels=labels, default=default_items)
        print(data)
        return JsonResponse(data)


def analysis(request):
    return render(request, 'GenderedTweetsUI/analysis.html', {})
