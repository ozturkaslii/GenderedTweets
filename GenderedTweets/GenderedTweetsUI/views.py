from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic

from GenderedTweetsUI.analyze import AnalyzeTweets


class IndexView(generic.ListView):

    def get(self, request):
        return render(request, 'GenderedTweetsUI/index.html')

    def get_data(request, *args, **kwargs):
        tweet = AnalyzeTweets()
        labels = tweet.tweet_label()
        default_items = tweet.tweet_count()
        data = dict(labels=labels, default=default_items)
        print(data)
        return JsonResponse(data)


class AnalysisView(generic.ListView):

    def get(self, request):
        return render(request, 'GenderedTweetsUI/analysis.html')

    def get_data(request, *args, **kwargs):
        labels = ['woman', 'man']
        default_items = [20, 10]
        data = dict(labels=labels, default=default_items)
        return JsonResponse(data)
