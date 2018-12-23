from django.views import generic
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Tweet
from GenderedTweetsUI.stream import TwitterStreamer


class IndexView(generic.ListView):
    stream = TwitterStreamer.fetch_tweet()

    def get_queryset(self):
        return Tweet.objects.all()


def analysis(request):
    return render(request, 'GenderedTweetsUI/analysis.html', {})
