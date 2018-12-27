from django.test import TestCase
from .models import Tweet

# Create your tests here.

class TwitterTest(TestCase):
    def test_get_from_db(self):
        tweet = Tweet.objects.all()
        self.assertGreater(len(tweet), 0, "Cant't get tweets from database.")
