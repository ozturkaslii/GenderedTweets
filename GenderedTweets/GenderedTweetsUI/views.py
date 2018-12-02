from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'GenderedTweetsUI/index.html', {})

def analysis(request):
    return render(request, 'GenderedTweetsUI/analysis.html', {})