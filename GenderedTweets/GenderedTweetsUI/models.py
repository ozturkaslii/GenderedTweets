from django.db import models


class Test(models.Model):
    col = models.CharField(max_length=10)
